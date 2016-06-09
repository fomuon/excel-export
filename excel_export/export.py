# -*- coding: utf-8 -*-

import sqlite3
import os
import codecs
import sys

type_map = {'T': 'TEXT', 'I': 'INTEGER', 'N': 'NUMERIC'}

def export_to_sqlfile(sqls, sql_file):
	with codecs.open(sql_file, "w", 'utf-8') as file_fd:
		for sql in sqls:
			file_fd.write(sql + "\n")
	
def export_to_sqlite3(sqls, db_file):
	if os.path.exists(db_file):
		os.remove(db_file)
		
	with sqlite3.connect(db_file) as con:
		for sql in sqls:
			try:
				con.execute(sql)
			except:
				print "execute sqlite: ", sql.encode('utf8')
				exc_type, exc_value, exc_traceback  = sys.exc_info()
				exc_value = "%s; %s" % (exc_value, sql.encode('utf8'))
				raise exc_type, exc_value, exc_traceback

def convert_to_sqls(tables):
	sqls = []
	
	for table_name, val in tables.items():
		columns = []
		for col_info in val[0]:
			columns.append("`%s` %s" % (col_info[0], type_map[col_info[1]]))
		
		sqls.append("CREATE TABLE `%s` (%s);" % (table_name, ",".join(columns)))
		
		for row in val[1]:
			values = _convert_values(val[0], row)
			sqls.append("INSERT INTO `%s` VALUES (%s);" % (table_name, ",".join(values)))
	
	return sqls

def _convert_values(col_infos, row):
	values = []
	
	for i in xrange(len(col_infos)):
		val = None
		if row[i] == None:
			val = 'null'
		else:
			if col_infos[i][1] == 'I':
				val = str(int(row[i]))
			elif col_infos[i][1] == 'T':
				val = "'%s'" % row[i]
			else:
				val = str(row[i])
			
		values.append(val)
		
	return values