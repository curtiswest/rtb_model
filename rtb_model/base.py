#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

DATABASE_ENVIRONMENT = config('DATABASE_ENVIRONMENT')

if DATABASE_ENVIRONMENT in ("PROD", "PRODUCTION"):
    database_url = config('PROD_DATABASE_URL')
    database_port = config('PROD_DATABASE_PORT')
    database_username = config('PROD_DATABASE_USERNAME')
    database_password = config('PROD_DATABASE_PASSWORD')
    database_name = config('PROD_DATABASE_NAME')
elif DATABASE_ENVIRONMENT in ("TEST", "TESTING"):
    database_url = config('TEST_DATABASE_URL')
    database_port = config('TEST_DATABASE_PORT')
    database_username = config('TEST_DATABASE_USERNAME')
    database_password = config('TEST_DATABASE_PASSWORD')
    database_name = config('TEST_DATABASE_NAME')

DATABASE_CONNECTION_URL = f'postgresql://{database_username}:' \
                          f'{database_password}@' \
                          f'{database_url}:{database_port}/{database_name}'

engine = create_engine(DATABASE_CONNECTION_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
