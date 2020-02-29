#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from uuid import uuid4

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from model import base


class Component(base.Base):
    __tablename__: str = "component"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    number = Column(Integer, unique=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f'C{self.number}: {self.name}'

    def __str__(self):
        return self.__repr__()
