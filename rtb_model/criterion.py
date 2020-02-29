#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from model import base


class Criterion(base.Base):
    __tablename__: str = "criterion"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    number = Column(Integer)
    name = Column(String, unique=True)
    short_name = Column(String, unique=True)
    component_id = Column(UUID(as_uuid=True), ForeignKey('component.id'))
    component = relationship("Component", backref=backref("component"))
    advice = Column(Text)
    introductory_text = Column(Text)

    def __repr__(self):
        return f'C{self.component.number}.R{self.number}: {self.name}'

    def __str__(self):
        return self.__repr__()
