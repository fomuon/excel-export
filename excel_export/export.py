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

def convert_to_sqls_for_sqlite(tables, **kwargs):
	exclude_info = kwargs.get("exclude_info", None)
	add_create_table = kwargs.get("add_create_table", False)
	
	type_map = {'T': 'TEXT', 'I': 'INTEGER', 'N': 'NUMERIC', 'D': 'REAL'}
	sqls = []
	
	for table_name in sorted(tables):
		if exclude_info and table_name in exclude_info[0]:
			continue
		
		val = tables[table_name]
		
		if exclude_info and exclude_info[1].has_key(table_name):
			val = _filter_columns(val, exclude_info[1][table_name])
		
		col_infos, values = val
		
		if len(col_infos) > 0:
			create_cols = []
			insert_cols = []
			
			for col_info in col_infos:
				col_type = type_map[col_info[1][0]]
				create_cols.append("`%s` %s" % (col_info[0], col_type))
				insert_cols.append("`%s`" % col_info[0])
				
			pks = [ x[0] for x in col_infos if x[3] ]
			if pks:
				create_cols.append('PRIMARY KEY (%s)' % ", ".join('`' + x + '`' for x in pks))
			
			if add_create_table:
				sqls.append("DROP TABLE IF EXISTS `%s`;" % table_name)
				sqls.append("CREATE TABLE `%s` (%s);" % (table_name, ",".join(create_cols)))
			
			for row in values:
				row_val = _convert_values(col_infos, row)
				sqls.append("INSERT INTO `%s`(%s) VALUES (%s);" % (table_name, ",".join(insert_cols), ",".join(row_val)))
	
	return sqls
	

def convert_to_sqls_for_mysql(tables, **kwargs):
	exclude_info = kwargs.get("exclude_info", None)
	add_create_table = kwargs.get("add_create_table", False)
	add_truncate = kwargs.get("add_truncate", False)
	extended_insert = kwargs.get("extended_insert", False)

	type_map = {'T': 'VARCHAR', 'I': 'INT', 'N': 'DECIMAL', 'D': 'DATETIME'}
	sqls = []

	for table_name in sorted(tables):
		if exclude_info and table_name in exclude_info[0]:
			continue
		
		val = tables[table_name]
		
		if exclude_info and exclude_info[1].has_key(table_name):
			val = _filter_columns(val, exclude_info[1][table_name])
		
		col_infos, values = val
		
		if len(col_infos) > 0:
			create_cols = []
			insert_cols = []
			
			for col_info in col_infos:
				col_type = type_map[col_info[1][0]]
				
				if col_type == 'VARCHAR':
					col_type = "VARCHAR(%d)" % col_info[1][1]
				elif col_type == 'DECIMAL':
					col_type = "DECIMAL(%d,%d)" % (col_info[1][1] + 3, col_info[1][1])
					
				create_cols.append("`%s` %s" % (col_info[0], col_type))
				insert_cols.append("`%s`" % col_info[0])
				
			pks = [ x[0] for x in col_infos if x[3] ]
			if pks:
				create_cols.append('PRIMARY KEY (%s)' % ", ".join('`' + x + '`' for x in pks))
			
			if add_create_table:
				sqls.append("DROP TABLE IF EXISTS `%s`;" % table_name)
				sqls.append("CREATE TABLE `%s` (%s);" % (table_name, ",".join(create_cols)))
			elif add_truncate:
				sqls.append("TRUNCATE `%s`;" % table_name)
			
			if extended_insert:
				for row in values:
					row_val = _convert_values(col_infos, row)
					sqls.append("INSERT INTO `%s`(%s) VALUES (%s);" % (table_name, ",".join(insert_cols), ",".join(row_val)))
			else:
				sql_row_vals = []
				for row in values:
					sql_row_vals.append("(%s)" % ",".join(_convert_values(col_infos, row)))
				
				sqls.append("INSERT INTO `%s`(%s) VALUES \n%s;" % (table_name, ",".join(insert_cols), ",\n".join(sql_row_vals)))
	
	return sqls

	pass

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

def _filter_columns(val, exclude_cols):
	exclude_indices = []
	filtered_head = []
	filtered_rows = []
	
	for idx, item in enumerate(val[0]):
		if item[0] in exclude_cols:
			exclude_indices.append(idx)
		else:
			filtered_head.append(item)
	
	for row in val[1]:
		filtered_row = []
		for idx, v in enumerate(row):
			if idx not in exclude_indices:
				filtered_row.append(v)
		
		filtered_rows.append(tuple(filtered_row))
		
	return (filtered_head, filtered_rows)