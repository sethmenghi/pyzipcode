from setuptools import setup, find_packages
import sys
import os

version = '0.52'

install_requires = [
    'Cython>=0.22',
    'numpy>=1.9.0',
    'pandas>=0.16.0',
    'mpld3',
    'IPython>=3.1.0',
    'sqlalchemy>=0.9.9',
    'psycopg2',
    'us']


setup(name='pyzipcode',
      version=version,
      description="query zip codes and location data",
      long_description=open("README.txt").read() + '\n\n' + open('CHANGES.txt').read(),
      keywords='zip code distance',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
