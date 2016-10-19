#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import extract, export
from excel_export import __version__

def main(argv):
	parser = argparse.ArgumentParser('excel-extract_tables', 'Export sql(sqlite, mysql) or db(sqlite) from specifically formatted excel file.')
	
	parser.add_argument('-I', '--input-files', nargs='+', type=str, help='Excel file path to export scripts. -I file1.xlsx file2.xlsx')
	
	group_sqlite = parser.add_argument_group('[For Sqlite]', 'Options for sqlite exporting.')
	group_sqlite.add_argument('--sqlite-output', default=None, type=str, help='Output FILE NAME for sqlite script.')
	group_sqlite.add_argument('--sqlite-add-create-table', default=False, action='store_true', help='Add DROP and CREATE TABLE statement in script file.')
	group_sqlite.add_argument('--sqlite-with-db-file', default=False, action='store_true', help='Enable Exporting DB file.')
	group_sqlite.add_argument('--sqlite-exclude', default=None, type=str, help='Add excluding tables and columns. --sqlite-exclude "table1,table2(col1,col2)"')
	
	group_mysql = parser.add_argument_group('[For MySql]', 'Options for mysql exporting.')
	group_mysql.add_argument('--mysql-output', default=None, type=str, help='Output FILE NAME for mysql script.')
	group_mysql.add_argument('--mysql-add-create-table', default=False, action='store_true', help='Add DROP and CREATE TABLE statement in script file.')
	group_mysql.add_argument('--mysql-add-truncate', default=False, action='store_true', help='Add TRUNCATE TABLE statement in script file.')
	group_mysql.add_argument('--mysql-extended-insert', default=False, action='store_true', help='Write INSERT statements using multiple-row syntax that includes several VALUES lists')
	group_mysql.add_argument('--mysql-exclude', default=None, type=str, help='Add excluding tables and columns. --sqlite-exclude "table1,table2(col1,col2)"')
	
	parser.add_argument('--version', default=False, action='store_true', help='Print the current version')
	
	args = parser.parse_args()
	
	if args.version:
		print('excel-export version {}'.format(__version__))
		exit(0)
	
	if args.input_files and (args.sqlite_output or args.mysql_output):
		all_tables = {}
		
		for excel_file in args.input_files:
			excel_file = unicode(excel_file, sys.getfilesystemencoding())
			print excel_file
			
			tables = extract.extract_tables_from_excel(excel_file)
			all_tables.update(tables)
		
		if args.sqlite_output:
			exclude_info = parse_exclude_info(args.sqlite_exclude) if args.sqlite_exclude else None
			sqls = export.convert_to_sqls_for_sqlite(all_tables, exclude_info=exclude_info, add_create_table=args.sqlite_add_create_table)
			
			export.export_to_sqlfile(sqls, args.sqlite_output)
			
			if args.sqlite_with_db_file and args.sqlite_add_create_table:
				export.export_to_sqlite3(sqls, args.sqlite_output + ".db")
			
			pass
		
		if args.mysql_output:
			exclude_info = parse_exclude_info(args.mysql_exclude) if args.mysql_exclude else None
			sqls = export.convert_to_sqls_for_mysql(all_tables, exclude_info=exclude_info, add_create_table=args.mysql_add_create_table, add_truncate=args.mysql_add_truncate, extended_insert=args.mysql_extended_insert)
			
			export.export_to_sqlfile(sqls, args.mysql_output)
			
			pass
	
	else:
		parser.print_help()
	
	pass

#추출시 제외할 정보 파서
#return (제외한 테이블, 제외할 컬럼) ( set(except_table), { table : set(except_cols) } )
def parse_exclude_info(exclude_arg):
	exclude_tables = set([])
	exclude_cols = {}
	
	last_elem = []
	in_bracket_tab = None
	
	for ch in exclude_arg:
		if ch == '(':
			in_bracket_tab = ''.join(last_elem).strip()
			if in_bracket_tab:
				exclude_cols[in_bracket_tab] = set([])
			last_elem = []
		elif ch == ')':
			if in_bracket_tab:
				v = ''.join(last_elem).strip()
				if v:
					exclude_cols[in_bracket_tab].add(v)
				
			last_elem = []
			in_bracket_tab = None
		elif ch == ',':
			v = ''.join(last_elem).strip()
			if v:
				if in_bracket_tab:
					exclude_cols[in_bracket_tab].add(v)
				else:
					exclude_tables.add(v)
				
			last_elem = []
		else:
			last_elem.append(ch)
	
	v = ''.join(last_elem).strip()
	if v:
		exclude_tables.add(v)
	
	
	return (exclude_tables, exclude_cols)

def entry_point():
	main(sys.argv[1:])

if __name__ == "__main__":
	entry_point()
	