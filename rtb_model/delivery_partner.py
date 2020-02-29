#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from . import base


class DeliveryPartner(base.Base):
    __tablename__: str = 'deliverypartner'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    prefix = Column(String(10))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    job_title = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f'Online User: {self.prefix} {self.first_name} {self.last_name}: {self.job_title} @ {self.email}'

    @property
    def full_name(self):
        if self.prefix:
            return f'{self.prefix} {self.first_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'
