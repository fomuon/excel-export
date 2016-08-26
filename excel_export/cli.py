#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import os
import extract, export
from excel_export import __version__

def main(argv):
	parser = argparse.ArgumentParser('excel-extract_tables', 'Export sql(sqlite, mysql) or db(sqlite) from specifically formatted excel file')
	
	parser.add_argument('-I', '--input-files', nargs='+', type=str, help='excel file path to extract sql. -I file1.xlsx file2.xlsx')
	parser.add_argument('-O', '--output-dir', default=os.getcwd(), help='output directory. default current directory')
	parser.add_argument('--with-mysql', default=False, action='store_true', help='create sql file for mysql')
	parser.add_argument('--with-db-file', default=False, action='store_true', help='create sqlite db file')
	parser.add_argument('--sqlite-exclude', default=None, type=str, help='[REMOVE_TAB_NAME],..., [TAB_NAME(REMOVE_COLUMN_NAME,...,)]')
	parser.add_argument('--version', default=False, action='store_true', help='Print the current version')
	
	args = parser.parse_args()
	
	if args.version:
		print('excel-export version {}'.format(__version__))
		exit(0)
	
	if args.sqlite_exclude:
		_parse_exclude_arg(args.sqlite_exclude)
		exit(0)
	
	if args.input_files:
		for excel_file in args.input_files:
			excel_file = unicode(excel_file, sys.getfilesystemencoding())
			
			tables = extract.extract_tables_from_excel(excel_file)
			
			sqls = export.convert_to_sqls(tables)
			
			file_name, file_ext = os.path.splitext(os.path.basename(excel_file))  # @UnusedVariable
			
			print excel_file, "===>"
			
			sql_file = os.path.join(args.output_dir, file_name + ".sql")
			export.export_to_sqlfile(sqls, sql_file)
			print "\t", sql_file
			
			if args.with_db_file:
				db_file = os.path.join(args.output_dir, file_name + ".db")
				export.export_to_sqlite3(sqls, db_file)
				print "\t", db_file
			
			if args.with_mysql:
				sql_file = os.path.join(args.output_dir, file_name + "_mysql.sql")
				sqls = export.convert_to_sqls(tables, 'mysql')
				export.export_to_sqlfile(sqls, sql_file)
				print "\t", sql_file
				
		print "Done!"
	else:
		parser.print_help()
	
	pass

#추출시 제외할 정보 파서
#return (제외한 테이블, 제외할 컬럼) ( set(except_table), { table : set(except_cols) } )
def _parse_exclude_arg(exclude_arg):
	exclude_tables = set([])
	exclude_cols = {}
	
	is_in_tab = None
	
	for info in exclude_arg.split(','):
		if '(' in info:
			tmp = info.split('(')
			exclude_cols[tmp[0]] = set([tmp[1].strip()])
			is_in_tab = tmp[0]
		elif ')' in info:
			exclude_cols[is_in_tab].add(info.split(')')[0].strip())
			is_in_tab = None
		elif is_in_tab:
			exclude_cols[is_in_tab].add(info.strip())
		else:
			exclude_tables.add(info.strip())
			
	
	print exclude_tables
	print exclude_cols
	
	return (exclude_tables, exclude_cols)
	pass

def entry_point():
	main(sys.argv[1:])

if __name__ == "__main__":
	entry_point()