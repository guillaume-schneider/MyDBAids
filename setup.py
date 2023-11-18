#!/usr/bin/env python

from distutils.core import setup

setup(name='mysql-generator-value',
      version='1.0',
      description='Python MySQL data Generator',
      author='Guillaume SCHNEIDER',
      author_email='guillaumeschneider@siggraph.org',
      packages=['mysqlgen', "mysqlgen.db", "mysqlgen.db.connector",
                "mysqlgen.stream"],
     )
