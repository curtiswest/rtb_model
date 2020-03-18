#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from . import base


class Measure(base.Base):
    __tablename__: str = "measure"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    number = Column(Integer)
    text = Column(String, unique=True)
    criterion_id = Column(UUID(as_uuid=True), ForeignKey('criterion.id'))
    criterion = relationship("Criterion", backref=backref("criterion"))
    description = Column(String)

    def __repr__(self):
        return f'C{self.criterion.component.number}.R{self.criterion.number}.M{self.number}: {self.text}'

    def __str__(self):
        return self.__repr__()
