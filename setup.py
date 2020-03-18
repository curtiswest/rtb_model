#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from setuptools import setup

setup(name='rtb_model',
      version='1.4',
      description='The data model backing Raise the BAR',
      url='git@github.com:curtiswest/rtb_model.git',
      author='Curtis West',
      author_email='curtis@curtiswest.net',
      license='None',
      packages=['rtb_model'],
      zip_safe=False,
      install_requires=['sqlalchemy', 'python-decouple', 'pandas', 'pytz', 'requests', 'psycopg2'])
