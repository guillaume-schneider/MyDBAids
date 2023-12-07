#!/usr/bin/env python

from distutils.core import setup

setup(name='mdba',
      version='1.0',
      description='MyDBAids is a dynamic Python tool designed for efficient data'
                  + 'generation and management. Featuring an intuitive command-line'
                  + 'interface, it allows seamless creation of custom data blueprints' 
                  + 'and leverages the Faker library for authentic data simulation,'
                   + 'making it an essential tool for developers and database professionals.',
      author='Guillaume SCHNEIDER',
      author_email='guillaumeschneider@siggraph.org',
      packages=['mdba', "mdba.db", "mdba.db.connector",
                "mdba.stream", "mdba.dependency", 
                "mdba.db.abstract",],
)
