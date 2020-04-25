#  Copyright (c) 2020 Curtis West <curtis@curtiswest.net>. All Rights Reserved

import requests
import json
import typing
import logging
import datetime as dt
import enum

import pytz
import pandas as pd


from decouple import config

logger = logging.getLogger(__name__)

# noinspection SpellCheckingInspection
API_ACCESS_TOKEN = config('FORMSTACK_API_ACCESS_TOKEN')
API_BASE_URL = config('FORMSTACK_API_BASE_URL')


class FormstackUtility:
    class CallMethod(enum.Enum):
        POST = requests.post
        PUT = requests.put
        DELETE = requests.delete
        GET = requests.get

    @staticmethod
    def _send_request(call_method: CallMethod, endpoint: str, return_json_content: bool, data: dict = None):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(API_ACCESS_TOKEN)}
        if data is not None:
            data = json.dumps(data)
        logging.debug(f'Sending request to Formstack via method {call_method}. Endpoint: {API_BASE_URL + endpoint}, \n\theaders: {headers}, \n\tdata: {data}')
        response = call_method(API_BASE_URL + endpoint, headers=headers, data=data)
        logging.debug(f'Received response from Formstack: {response} w/ content: {response.content}')

        # TODO: HTTP status code check and error handling on response
        if return_json_content:
            return json.loads(response.content.decode('utf-8'))
        else:
            return response

    @staticmethod
    def get_formstack(endpoint: str, return_json_content: bool = True):
        return FormstackUtility.get(endpoint=endpoint, return_json_content=return_json_content)

    @staticmethod
    def get(endpoint: str, return_json_content=True):
        return FormstackUtility._send_request(call_method=FormstackUtility.CallMethod.GET,
                                              endpoint=endpoint,
                                              return_json_content=return_json_content)

    @staticmethod
    def post(endpoint: str, data: dict, return_json_content=True):
        return FormstackUtility._send_request(call_method=FormstackUtility.CallMethod.POST,
                                              endpoint=endpoint,
                                              return_json_content=return_json_content,
                                              data=data)

    @staticmethod
    def delete(endpoint: str, return_json_content=True):
        return FormstackUtility._send_request(call_method=FormstackUtility.CallMethod.DELETE,
                                              endpoint=endpoint,
                                              return_json_content=return_json_content)

    @staticmethod
    def put(endpoint: str, data: dict, return_json_content=True):
        return FormstackUtility._send_request(call_method=FormstackUtility.CallMethod.PUT,
                                              endpoint=endpoint,
                                              return_json_content=return_json_content,
                                              data=data)


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

    def get_fields(self) -> typing.Optional[pd.DataFrame]:
        df = pd.DataFrame(self._json_data['fields'])
        if len(df) > 0:
            df['id'] = df['id'].astype(int)
            return df[df['type'] != 'section'][['id', 'label', 'description']].set_index('id')
        else:
            return None

    def refresh(self) -> None:
        logger.info(f'Refreshing form {self.form_id}')
        self._json_data = FormstackUtility.get(f'form/{self.form_id}', return_json_content=True)

    def get_all_submission_ids(self) -> typing.List[int]:
        return [int(i['id']) for i in
                FormstackUtility.get(f'form/{self.form_id}/submission'
                                               , return_json_content=True)['submissions']]

    def delete_field(self, field_id: int):
        return FormstackUtility.delete(f'field/{field_id}', return_json_content=True)

    def get_field(self, field_id: int):
        return FormstackUtility.get(f'field/{field_id}', return_json_content=True)

    def add_field(self, field_type: str, label: str, hide_label: bool = None, description: str = None,
                  description_callout: bool = None, default_value: str = None, options: typing.List[str] = None,
                  options_values: typing.List[str] = None, required: bool = None, read_only: bool = None,
                  hidden: bool = None, unique: bool = None, column_span: int = None, sort: int = None,
                  attributes: dict = None, logic: dict = None, calculation: str = None):
        data = {'field_type': field_type,
                'label': label,
                'hide_label': "1" if hide_label else "0",
                'description': description,
                'description_callout': "1" if description_callout else "0",
                'default_value': default_value,
                'required': "1" if required else "0",
                'readonly': "1" if read_only else "0",
                'hidden': "1" if hidden else "0",
                'uniq': "1" if unique else "0",
                'options':  options,
                'options_values': options_values,
                'colspan': column_span,
                'sort': sort,
                'attributes': attributes,
                'logic': logic,
                'calculation': calculation,
                }

        return FormstackUtility.post(f'form/{self.form_id}/field', data=data)

    def update_field(self, field_id: int, field_type: str = None, label: str = None,
                     hide_label: bool = None, description: str = None,
                  description_callout: bool = None, default_value: str = None, options: typing.List[str] = None,
                  options_values: typing.List[str] = None, required: bool = None, read_only: bool = None,
                  hidden: bool = None, unique: bool = None, column_span: int = None, sort: int = None,
                  attributes: dict = None, logic: dict = None, calculation: str = None):
        data = dict()
        if field_type is not None:
            data['field_type'] = field_type
        if label is not None:
            data['label'] = label
        if hide_label is not None:
            data['hide_label'] = "1" if hide_label else "0"
        if description is not None:
            data['description'] = description
        if description_callout is not None:
            data['description_callout'] =  "1" if description_callout else "0"
        if default_value is not None:
            data['default_value'] = default_value
        if required is not None:
            data['required'] = "1" if required else "0"
        if read_only is not None:
            data['readonly'] = "1" if read_only else "0"
        if hidden is not None:
            data['hidden'] = "1" if hidden else "0"
        if unique is not None:
            data['uniq'] = "1" if unique else "0"
        if options is not None:
            data['options'] = options
        if options_values is not None:
            data['options_values'] = options_values
        if column_span is not None:
            data['colspan'] = column_span
        if sort is not None:
            data['sort'] = sort
        if attributes is not None:
            data['attributes'] = attributes
        if logic is not None:
            data['logic'] = logic
        if calculation is not None:
            data['calculation'] = calculation

        return FormstackUtility.put(f'field/{field_id}', data=data)


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
