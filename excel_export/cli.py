#!/usr/bin/env python
# encoding: utf-8
import sys
import argparse
import os
import extract, export
from excel_export import __version__

def main(argv):
	parser = argparse.ArgumentParser('excel-extract_tables', 'Extract Sql (mysql or sqlite) from specifically formatted excel file')
	
	parser.add_argument('-I', '--input-files', nargs='+', type=str, help='excel file path to extract sql. -I file1.xlsx file2.xlsx')
	parser.add_argument('-O', '--output-dir', default=os.getcwd(), help='output directory. default current directory')
# 	parser.add_argument('-T', '--output-type', default='all', choices=['mysql', 'sqlite', 'all'])
# 	parser.add_argument('--without-mysql-ddl', default=False, help='generate create table statement for mysql')
# 	parser.add_argument('--without-sqlite-ddl', default=False, help='generate create table statement for sqlite')
# 	parser.add_argument('--without-sqlite-db', default=False, help='create sqlite db file')
	parser.add_argument('--version', default=False, action='store_true', help='Print the current version')
	
	args = parser.parse_args()
	
	if args.version:
		print('excel-export version {}'.format(__version__))
		exit(0)
	
	if args.input_files:
		for excel_file in args.input_files:
			tables = extract.extract_tables_from_excel(excel_file)
			file_name, file_ext = os.path.splitext(os.path.basename(excel_file))  # @UnusedVariable
			output_files = export.export_to_sqlite3(tables, args.output_dir, file_name)
		
			print excel_file, "===>"
			for file_path in output_files:
				print "\t", file_path
		print "Done!"
	else:
		parser.print_help()
	
	pass

def entry_point():
	main(sys.argv[1:])

if __name__ == "__main__":
	entry_point()