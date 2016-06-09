#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import os
import extract, export
from excel_export import __version__

def main(argv):
	parser = argparse.ArgumentParser('excel-extract_tables', 'Extract sql or db(sqlite) from specifically formatted excel file')
	
	parser.add_argument('-I', '--input-files', nargs='+', type=str, help='excel file path to extract sql. -I file1.xlsx file2.xlsx')
	parser.add_argument('-O', '--output-dir', default=os.getcwd(), help='output directory. default current directory')
	parser.add_argument('--with-db-file', default=False, action='store_true', help='create sqlite db file')
	parser.add_argument('--version', default=False, action='store_true', help='Print the current version')
	
	args = parser.parse_args()
	
	if args.version:
		print('excel-export version {}'.format(__version__))
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
		
		print "Done!"
	else:
		parser.print_help()
	
	pass

def entry_point():
	main(sys.argv[1:])

if __name__ == "__main__":
	entry_point()