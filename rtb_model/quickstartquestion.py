#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from __future__ import annotations
from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from . import base
from .component import Component


class QuickstartQuestion(base.Base):
    __tablename__: str = 'quickstartquestion'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    question_text = Column(String, nullable=False)
    formstack_form_id = Column(Integer, nullable=False)

    component_id = Column(UUID(as_uuid=True), ForeignKey('component.id'))
    component: Component = relationship("Component", backref=backref("component_quickstartquestion"))

    def __repr__(self):
        return f'Quickstart question: {self.question_text} related to component #{self.component.number}'
