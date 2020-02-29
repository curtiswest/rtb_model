#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

import typing
from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from Formstack import FormstackSubmission
from model import base


class OnlineUser(base.Base):
    __tablename__: str = 'onlineuser'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    prefix = Column(String(10))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    job_title = Column(String)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'))
    company = relationship("Company", backref=backref("company"))

    def __repr__(self):
        return f'Online User: {self.prefix} {self.first_name} {self.last_name}: {self.job_title} @ {self.email}'

    @staticmethod
    def extract_name_parts(from_str):
        prefix, first_name, last_name = from_str.split('\n')
        prefix = prefix.replace('prefix = ', '')
        first_name = first_name.replace('first = ', '')
        last_name = last_name.replace('last = ', '')

        return prefix, first_name, last_name

    @classmethod
    def from_formstack(cls, formstack_submission: FormstackSubmission) -> typing.List:
        field_map = {
            1: {'name': 87125327,
                'email': 87125332,
                'job_title': 87125333},
            2: {'name': 87125336,
                'email': 87125337,
                'job_title': 87125338},
            3: {'name': 87125340,
                'email': 87125341,
                'job_title': 87125342},
            4: {'name': 87125344,
                'email': 87125345,
                'job_title': 87125346},
            5: {'name': 87125351,
                'email': 87125352,
                'job_title': 87125353},
        }

        data = formstack_submission.get_data()
        num_users = int(data.loc[87125326].value)
        users = list()

        for i in range(1, num_users + 1):
            prefix, first_name, last_name = OnlineUser.extract_name_parts(data.loc[field_map[i]['name']].value)
            email = data.loc[field_map[i]['email']].value
            job_title = data.loc[field_map[i]['job_title']].value
            # noinspection PyArgumentList
            users.append(cls(prefix=prefix, first_name=first_name, last_name=last_name,
                             email=email, job_title=job_title))

        return users
