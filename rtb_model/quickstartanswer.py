#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from __future__ import annotations
import enum
from uuid import uuid4


from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from . import base

class QuickstartLikertAnswer(enum.Enum):
    strongly_disagree = 1
    disagree = 2
    unsure = 3
    agree = 4
    strongly_agree = 5

class QuickstartAnswer(base.Base):
    __tablename__: str = 'quickstartanswer'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    quickstart_user_id = Column(UUID(as_uuid=True), ForeignKey('quickstartuser.id'))
    quickstart_user = relationship("QuickstartUser", backref=backref("quickstartuser"))

    question_id = Column(UUID(as_uuid=True), ForeignKey('quickstartquestion.id'))
    question = relationship('QuickstartQuestion', backref=backref("quickstartquestion"))

    answer = Column(Enum(QuickstartLikertAnswer))

    def __repr__(self):
        return f'Quickstart result: {self.quickstart_user} A: {self.answer}'
