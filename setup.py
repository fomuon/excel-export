#!/usr/bin/env
# encoding: utf-8

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

from excel_export import __version__
setup(
	name = "excel-export",
	version = __version__,
	packages = ["excel_export"],
	package_dir = {"excel_export": "excel_export"},
	install_requires = ["xlrd"],
	license = "BSD",
	author = "Lee,Yongkyu",
	author_email = "fomuon@gmail.com",
	url="https://github.com/fomuon/excel-export",
	entry_points = { "console_scripts": ["excel-export = excel_export.cli:entry_point"] },
	description = "A command-line tool (and python library) to extract sqlite db from excel files",
	long_description = "https://github.com/fomuon/excel-export",
	keywords = ["excel-export", "excel", "sqlite"]
)
