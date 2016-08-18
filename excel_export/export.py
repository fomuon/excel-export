# -*- coding: utf-8 -*-

import sqlite3
import os
import codecs
import sys

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

def convert_to_sqls(tables, db_type='sqlite', drop_if_exists=True):
	type_maps = { 
		'sqlite' : {'T': 'TEXT', 'I': 'INTEGER', 'N': 'NUMERIC', 'D': 'REAL'},
		'mysql' : {'T': 'VARCHAR', 'I': 'INT', 'N': 'DECIMAL', 'D': 'DATETIME'}
	}
	
	type_map = type_maps[db_type]
	sqls = []
	
	for table_name in sorted(tables):
		val = tables[table_name]
		columns = []
		
		for col_info in val[0]:
			col_type = type_map[col_info[1][0]]
			if db_type == 'mysql':
				if col_type == 'VARCHAR':
					col_type = "VARCHAR(%d)" % col_info[1][1]
				elif col_type == 'DECIMAL':
					col_type = "DECIMAL(%d,%d)" % (col_info[1][1] + 3, col_info[1][1])
				
			columns.append("`%s` %s" % (col_info[0], col_type))
			
		pks = [ x[0] for x in val[0] if x[3] ]
		if pks:
			columns.append('PRIMARY KEY (%s)' % ", ".join('`' + x + '`' for x in pks))
		
		if drop_if_exists:
			sqls.append("DROP TABLE IF EXISTS `%s`;" % table_name)
		
		sqls.append("CREATE TABLE `%s` (%s);" % (table_name, ", ".join(columns)))
		
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
			if col_infos[i][1][0] == 'I':
				val = str(int(row[i]))
			elif col_infos[i][1][0] == 'T' or col_infos[i][1][0] == 'D':
				val = "'%s'" % row[i]
			else:
				val = str(row[i])
			
		values.append(val)
		
	return values