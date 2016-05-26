#!/usr/bin/env
# encoding: utf-8
from setuptools import setup

try:
	with open('README.rst') as f:
		readme = f.read()
except IOError:
	readme = ''

setup(
	name="excel-export",
	version='0.1.0',
	author='Lee,Yongkyu',
	author_email='fomuon@gmail.com',
	url='https://github.com/fomuon/excel-export',
	entry_points = { 'console_scripts': ['excel-export = excel_export.cli:entry_point'] },
	packages = ['excel_export'],
	description="A command-line tool (and python library) to extract sqlite db from excel files",
	long_description=readme,
	license = 'BSD',
	install_requires=["xlrd"],
)