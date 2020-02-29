#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from uuid import uuid4

from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from model import base


class Answer(base.Base):
    __tablename__ = 'answer'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    response = Column(Enum('Yes', 'No', 'Unsure', 'Not applicable', name='answer_response'))

    # Relationship to Submission
    formstack_submission_id = Column(Integer, ForeignKey('formstacksubmission.id'))
    formstack_submission = relationship("FormstackSubmission", backref=backref("formstacksubmission"))

    # Relationship to Measure
    measure_id = Column(UUID(as_uuid=True), ForeignKey('measure.id'))
    measure = relationship("Measure", backref=backref("measure"))

    # Relationship to OnlineUser
    online_user_id = Column(UUID(as_uuid=True), ForeignKey('onlineuser.id'))
    online_user = relationship("OnlineUser", backref=backref("onlineuser"))

    def __repr__(self):
        return f'Response: {self.response} to measure: {self.measure} by user: {self.online_user.first_name} {self.online_user.last_name}'

    def __str__(self):
        return self.__repr__()
