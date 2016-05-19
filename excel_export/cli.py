#!/usr/bin/env python
# encoding: utf-8
import sys
import argparse

def main(argv):
	parser = argparse.ArgumentParser('excel-export', 'Extract Sql (mysql or sqlite) from specifically formatted excel file')
	
	parser.add_argument('--version', default=False, action='store_true', help='Print the current version')
	
	
	args = parser.parse_args()
	
	pass

def entry_point():
	main(sys.argv[1:])

if __name__ == "__main__":
	entry_point()