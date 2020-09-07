#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from __future__ import annotations
from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from .formstack_utilities import FormstackSubmissionHelper
from . import base


class QuickstartUser(base.Base):
    __tablename__: str = 'quickstartuser'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    job_title = Column(String)
    online_user_id = Column(UUID(as_uuid=True), ForeignKey('onlineuser.id'))
    online_user = relationship("OnlineUser", backref=backref("onlineuser"))

    def __repr__(self):
        return f'Quickstart User: {self.first_name} {self.last_name}: {self.job_title} @ {self.email}'

    @classmethod
    def from_formstack(cls, formstack_submission: FormstackSubmissionHelper) -> QuickstartUser:
        data = formstack_submission.get_data()

        field_map = {'first_name': 96828995,
                     'last_name': 96829050,
                     'email': 96828832,
                     'job_title': 96828834}

        first_name = data.loc[field_map['email']].value
        last_name = data.loc[field_map['last_name']].value
        email = data.loc[field_map['email']].value
        job_title = data.loc[field_map['job_title']].value

        # noinspection PyArgumentList
        return cls(first_name=first_name, last_name=last_name, email=email, job_title=job_title)

