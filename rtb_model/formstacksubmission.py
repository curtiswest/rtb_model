#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from sqlalchemy import Column, Integer, DateTime

from . import base


class FormstackSubmission(base.Base):
    __tablename__: str = "formstacksubmission"
    id = Column(Integer, primary_key=True)
    date_submit = Column(DateTime)
    date_last_update = Column(DateTime)
