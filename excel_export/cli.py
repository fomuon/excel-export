#!/usr/bin/env python
# encoding: utf-8
import sys
import argparse
import os
from excel_export import core

def main(argv):
	parser = argparse.ArgumentParser('excel-export', 'Extract Sql (mysql or sqlite) from specifically formatted excel file')
	
	parser.add_argument('-I', '--input-file', help='excel file path to extract sql')
	parser.add_argument('-O', '--output-dir', default=os.getcwd(), help='output directory. default current directory')
	parser.add_argument('-T', '--output-type', default='all', choices=['mysql', 'sqlite', 'all'])
	parser.add_argument('--without-mysql-ddl', default=False, help='generate create table statement for mysql')
	parser.add_argument('--without-sqlite-ddl', default=False, help='generate create table statement for sqlite')
	parser.add_argument('--without-sqlite-db', default=False, help='create sqlite db file')
	parser.add_argument('--version', default=False, action='store_true', help='Print the current version')
	
	args = parser.parse_args()
	
	print args
	core.export(excel_file=args.input_file, output_dir=args.output_dir, output_type=args.output_type)
	
	pass

def entry_point():
	main(sys.argv[1:])

if __name__ == "__main__":
	entry_point()