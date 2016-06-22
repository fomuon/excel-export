# -*- coding: utf-8 -*-
import xlrd


def extract_tables_from_excel(excel_file):
	tables_in_all_sheet = {}
	
	workbook = xlrd.open_workbook(excel_file)
	
	for sheet in workbook.sheets():
		if sheet.ncols > 0:
			tables_in_sheet = _get_tables_in_sheet(sheet)
			tables_in_all_sheet.update(tables_in_sheet)
			print len(tables_in_sheet), "tables extracted in sheet(", sheet.name.encode('utf8'), ")"
		
	return tables_in_all_sheet;

def _get_tables_in_sheet(sheet):
	'''
	sheet 내 정보를 추출한다.
	'''
	merged_heads = []
	merged_single_col_ranges = [] #1열이 수직으로 병함된 셀정보. 동일값 처리
	
	for crange in sheet.merged_cells:
		if crange[0] == 0 and crange[1] == 1:
			merged_heads.append((crange[2], crange[3]))
		if crange[2] + 1 == crange[3]:
			merged_single_col_ranges.append(crange)
	
	merged_heads.sort(reverse=True)
	
	s_col_idx = e_col_idx = 0
	merged_range = None
	header_infos = [] #list of tuple (table name, start_col_idx, end_col_idx)
	
	while True:
		if not merged_range and len(merged_heads) > 0:
			merged_range = merged_heads.pop()
			
		if merged_range and merged_range[0] <= s_col_idx < merged_range[1]:
			e_col_idx = merged_range[1] - 1
			merged_range = None
		else:
			e_col_idx = s_col_idx
		
		s_cell_val = sheet.cell(0, s_col_idx).value
		arr_val = s_cell_val.split(':') if ':' in s_cell_val else None
		
		if arr_val and arr_val[0].strip() == 'EXP':
			table_name = arr_val[1].strip()
			header_infos.append((table_name, s_col_idx, e_col_idx))
		
		s_col_idx = e_col_idx + 1
		if s_col_idx >= sheet.ncols:
			break
	
	tables = {}
	#return header_infos
	for header_info in header_infos:
		table = _get_table(sheet, header_info, merged_single_col_ranges)
		tables[header_info[0]] = table
		
	return tables
	
def _get_table(sheet, header_info, merged_single_col_ranges):
	"""
	header_info를 바탕으로 sheet로부터 테이블 데이터(헤더정보포함) 추출한다
	"""
	cols = [] 
	data_row_pos = 0
	for col_idx in xrange(header_info[1], header_info[2] + 1):
		col1 = sheet.cell(1, col_idx).value
		col2 = sheet.cell(2, col_idx).value
		
		arr_col = None
		
		if ':' in col1:
			arr_col = col1.split(':')
			if data_row_pos == 0: data_row_pos = 2
		elif ':' in col2:
			arr_col = col2.split(':')
			if data_row_pos == 0: data_row_pos = 3
		
		if arr_col:
			pk = True if len(arr_col) == 3 and arr_col[2] == 'PK' else False
			cols.append([arr_col[0].strip(), arr_col[1].strip(), col_idx, pk, 0])
	
	data_rows = []
	
	while data_row_pos < sheet.nrows:
		row = []
		for col in cols:
			rng = _check_merged_cell(merged_single_col_ranges, data_row_pos, col[2])
			
			if rng:
				val = sheet.cell(rng[0], rng[2]).value
			else:
				val = sheet.cell(data_row_pos, col[2]).value
			
			if col[1] == 'T': #문자열 타입이면 항목중 가장 긴 문자열의 길이를 구함.
				val_size = len(val) if type(val) == unicode else len(str(val))
				col[4] = val_size if val_size > col[4] else col[4]
			elif col[1] == 'N': #소수표현이라면 소수점 이하 길이를 구함.
				str_val = str(val).strip()
				fraction_len = len(str_val[str_val.find('.')+1:]) if str_val.find('.') >= 0 else 0
				col[4] = fraction_len if fraction_len > col[4] else col[4]
				
			row.append(None if val == '' else val)
			
		if _check_all_none(row):
			break
		
		data_rows.append(tuple(row))
		data_row_pos += 1
	
	col_infos = [] # list of tuple (column name, data type, col_idx, pk)
	
	for col in cols:
		col[1] = (col[1], col[4]) if col[1] == 'T' or col[1] == 'N' else (col[1],)
		col_infos.append(tuple(col[:-1]))
	
	return (col_infos, data_rows)

def _check_all_none(itarable):
	for elem in itarable:
		if elem != None:
			return False
	return True

def _check_merged_cell(merged_single_col_ranges, row, col):
	"""
	merged_single_col_ranges 중 cell(row,col)을 포함하는 범위가 있으면 리턴
	"""
	for rng in merged_single_col_ranges:
		if col == rng[2] and row >= rng[0] and row < rng[1]:
			return rng
	