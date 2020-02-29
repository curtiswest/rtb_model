#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

import datetime as dt
from uuid import uuid4

from sqlalchemy import Boolean, CHAR, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import BIGINT, UUID

from model import base
from Formstack import FormstackSubmission


class Company(base.Base):
    __tablename__: str = 'company'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_name = Column(String)
    abn = Column(BIGINT)
    abs_group = Column(CHAR)
    abs_subdivision = Column(Integer)
    business_size = Column(String)
    operate_australia = Column(Boolean)
    operate_new_zealand = Column(Boolean)
    operate_internationally = Column(Boolean)
    operate_other = Column(String)
    annual_turnover = Column(String)
    submission_id = Column(Integer)
    date_submit = Column(DateTime)
    date_last_update = Column(DateTime)
    date_complete = Column(DateTime, nullable=True)

    # managing_delivery_partner_id = Column(UUID(as_uuid=True), ForeignKey('deliverypartner.id'))
    # managing_delivery_partner = relationship("DeliveryPartner", backref=backref("deliverypartner"))

    def __str__(self):
        return f"{self.company_name}: ABN #{self.abn}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_formstack(cls, formstack_submission: FormstackSubmission):
        data = formstack_submission.get_data()

        abs_group_to_field_id = {
            'A': 87125025,
            'B': 87125166,
            'C': 87125193,
            'D': 87125210,
            'E': 87125234,
            'F': 87125236,
            'G': 87125237,
            'H': 87125239,
            'I': 87125245,
            'J': 87125246,
            'K': 87125248,
            'L': 87125249,
            'M': 87125250,
            'N': 87125253,
            'O': 87125254,
            'P': 87125255,
            'Q': 87125256,
            'R': 87125257,
            'S': 87125257,
        }
        operate_locations = data.loc[87125313].value.split('\n')
        params = {'company_name': data.loc[87125019].value, 'abn': data.loc[87125021].value,
                  'abs_group': data.loc[87125022].value.strip()[0], 'business_size': data.loc[87125270].value,
                  'operate_australia': 'Australia' in operate_locations,
                  'operate_new_zealand': 'New Zealand' in operate_locations,
                  'operate_internationally': 'Internationally' in operate_locations,
                  'operate_other': [x for x in operate_locations if
                                    x not in ['Australia', 'New Zealand', 'Internationally']],
                  'annual_turnover': data.loc[87125311].value, 'submission_id': formstack_submission.submission_id,
                  'date_submit': formstack_submission.timestamp,
                  'date_last_update': dt.datetime.utcnow()
                  }
        params['abs_subdivision'] = data.loc[abs_group_to_field_id[params['abs_group']]].value.strip()[1:3]

        # noinspection PyArgumentList
        return cls(**params)
