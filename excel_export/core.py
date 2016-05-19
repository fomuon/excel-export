#!/usr/bin/env python
# encoding: utf-8
import xlrd
import os

def export(**kwargs):
	excel_file = kwargs.get('excel_file')
	output_dir = kwargs.get('output_dir')
	output_type = kwargs.get('output_type')
	
	workbook = xlrd.open_workbook(excel_file)
	
	for sheet in workbook.sheets():
		print "\nWorkSheet[", sheet.name.encode('utf8'), "] 탐색..."
		
		if sheet.ncols > 0:
			data = _get_tables_in_sheet(sheet)
	
	print excel_file, output_dir
	pass

def _get_tables_in_sheet(sheet):
	'''
	sheet 내 정보를 추출한다.
	'''
	merged_heads = []
	
	for crange in sheet.merged_cells:
		if crange[0] == 0 and crange[1] == 1:
			merged_heads.append((crange[2], crange[3]))
	
	merged_heads.sort(reverse=True)
	print merged_heads
	
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
	
	#return header_infos
	for header_info in header_infos:
		table = _get_table(sheet, header_info)
	
def _get_table(sheet, header_info):
	cols = []
	for col_idx in xrange(header_info[1], header_info[2] + 1):
		col1 = sheet.cell(1, col_idx).value
		col2 = sheet.cell(2, col_idx).value
		
		arr_col = None
		
		if ':' in col1:
			arr_col = col1.split(':')
		elif ':' in col2:
			arr_col = col2.split(':')
		
		if arr_col:
			cols.append((arr_col[0].strip(), arr_col[1].strip(), col_idx))
	
	print "========="
	print header_info
	print cols
	
	
	return
