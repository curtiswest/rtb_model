#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

import requests
import json
import typing
import logging
import datetime as dt

import pytz
import pandas as pd

from decouple import config

logger = logging.getLogger(__name__)

# noinspection SpellCheckingInspection
API_ACCESS_TOKEN = config('FORMSTACK_API_ACCESS_TOKEN')
API_BASE_URL = config('FORMSTACK_API_BASE_URL')


class FormstackUtility:
    @staticmethod
    def get_formstack(endpoint, return_json_content=True):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(API_ACCESS_TOKEN)}
        response = requests.get(API_BASE_URL + endpoint, headers=headers)

        # TODO: HTTP status code check and error handling on response
        if return_json_content:
            return json.loads(response.content.decode('utf-8'))
        else:
            return response


class FormstackForm:
    _form_id = None
    _json_data = None
    _fields = None

    @property
    def form_id(self):
        return self._form_id

    @form_id.setter
    def form_id(self, value):
        self._form_id = value
        self.refresh()

    def __init__(self, form_id):
        self.form_id = form_id

    def get_fields(self) -> pd.DataFrame:
        df = pd.DataFrame(self._json_data['fields'])
        df['id'] = df['id'].astype(int)
        return df[df['type'] != 'section'][['id', 'label', 'description']].set_index('id')

    def refresh(self) -> None:
        logger.info(f'Refreshing form {self.form_id}')
        self._json_data = FormstackUtility.get_formstack(f'form/{self.form_id}', return_json_content=True)

    def get_all_submission_ids(self) -> typing.List[int]:
        return [int(i['id']) for i in
                FormstackUtility.get_formstack(f'form/{self.form_id}/submission'
                                               , return_json_content=True)['submissions']]


class FormstackSubmissionHelper:
    form = None
    _submission_id = None
    json_data = None

    @property
    def portal_participant_email(self):
        return self.json_data['portal_participant_email']

    @property
    def submission_id(self) -> int:
        return self._submission_id

    @submission_id.setter
    def submission_id(self, value: int):
        self._submission_id = int(value)
        self.refresh()

    def __init__(self, submission_id: int):
        self.submission_id = submission_id

    def refresh(self) -> None:
        logger.info(f'Refreshing submission {self.submission_id}')
        self.json_data = FormstackUtility.get_formstack(f'submission/{self.submission_id}', return_json_content=True)

        if self.form is None or self.form.form_id != self.json_data['form']:
            self.form = FormstackForm(self.json_data['form'])

    def get_data(self, with_labels=True) -> pd.DataFrame:
        if with_labels:
            field_labels = self.form.get_fields()
            data = pd.DataFrame(self.json_data['data'])
            data['field'] = data['field'].astype(int)
            data = data.set_index('field')
            return field_labels.join(data)
        else:
            # TODO: make returned index fields consistent
            return pd.DataFrame(self.json_data['data']).set_index('field')

    @property
    def portal_email(self) -> typing.Union[None, str]:
        try:
            return self.json_data['portal_participant_email']
        except KeyError as e:
            logger.error(e)
            return None

    @property
    def timestamp(self) -> dt.datetime:
        """
        Returns the timestamp of this submission in UTC.
        :return: timestamp of this submission in UTC.
        """
        ts = self.json_data['timestamp']
        # Extract the datetime object from the `ts` string
        ts = dt.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        # Localise to Eastern time (Formstack returns Eastern times)
        ts = pytz.timezone('US/Eastern').localize(ts)
        # Convert to UTC time
        return ts.astimezone(pytz.timezone('UTC'))
