import json

from utils.attr_dict import AttrDict
from utils.http_request import make_http_post_request, make_http_get_request, make_http_patch_request
from utils.common import AIRTABLE_URL, MAX_API_ATTEMPTS


class Webhook():

    def create(self, api_key, form, webhook):
        print(f'airtable create function call.')
        api_attempts = 1
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        url = f"{AIRTABLE_URL}{form.airtable_base}/{form.airtable_table}"

        # Getting fields mappings by comparing form fields with webhook
        _, fields = self.get_mapping_fields_dict(form, webhook)

        # creating payload here.
        data = {
            'records':
                [
                    {
                        'fields': fields
                    }
                ]
        }

        # Encode json data payload.
        data = json.dumps(data)

        print(f'sending airtable create request. url [{url}], payload [{data}]')

        # We are checking status code here, if 5xx status code we got we iterate to 5 times.
        while True:
            print(f'airtable create request attempt: {api_attempts}')
            if api_attempts > MAX_API_ATTEMPTS:
                raise Exception('Api call exceeded.')
            resp = make_http_post_request(url, data, headers)
            print(f'airtable create request completed. url [{url}, '
                  f'status code [{resp.status_code}], response [{resp.content}]')

            # if status code start with 5, it updates api_attempts and retry again.
            if str(resp.status_code).startswith('5'):
                api_attempts += 1
            else:
                # Decode result content.
                return json.loads(resp.content)

    def update(self, api_key, form, webhook):
        print(f'airtable update function call.')
        api_attempts = 1
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        base_url = f"{AIRTABLE_URL}{form.airtable_base}/{form.airtable_table}"

        # Getting fields mappings by comparing form fields with webhook
        ref_id, fields = self.get_mapping_fields_dict(form, webhook)
        url_with_query_string = base_url + f"?maxRecords=1&filterByFormula={{Ref}}={ref_id}"
        print(f'fetch airtable record request. url [{url_with_query_string}]')

        # Getting the record with ref_id, because we want 'id' for that record
        resp = make_http_get_request(url_with_query_string, headers)
        print(f'fetch airtable record request completed. url [{url_with_query_string}, '
              f'status code [{resp.status_code}], response [{resp.content}]')

        # Decode result content and converting to dict like so that we can access it
        # attribute like.
        result = AttrDict(json.loads(resp.content))

        # Checking if record exists or not with given ref_id
        if len(result.records) == 0:
            print(f'No record found with this ref: {ref_id}')
            raise Exception(f'No record found with this ref: {ref_id}')
        record_id = result.records[0]['id']

        # creating payload here.
        data = {
            'records':
                [
                    {
                        "id": record_id,
                        'fields': fields
                    }
                ]
        }

        # Encode json data payload.
        data = json.dumps(data)

        print(f'sending airtable update request. url [{base_url}], payload [{data}]')

        # We are checking status code here, if 5xx status code we got we iterate to 5 times.
        while True:
            print(f'airtable update request attempt: {api_attempts}')
            if api_attempts > MAX_API_ATTEMPTS:
                raise Exception('Api call exceeded.')
            resp = make_http_patch_request(base_url, data, headers)
            print(f'airtable update request completed. url [{base_url}, '
                  f'status code [{resp.status_code}], response [{resp.content}]')

            # if status code start with 5, it updates api_attempts and retry again.
            if str(resp.status_code).startswith('5'):
                api_attempts += 1
            else:
                # Decode result content.
                return json.loads(resp.content)

    def get(self):
        pass

    def list(self):
        pass

    def delete(self):
        pass

    def get_mapping_fields_dict(self, form, webhook):
        fields = {}
        ref_id = None
        for mapping in form.mappings:
            mapping_dict = AttrDict(mapping)
            for data in webhook.data:
                data_dict = AttrDict(data)
                if mapping_dict.form_field_key == data_dict.key:
                    if mapping_dict.airtable_field_name == 'Ref':
                        ref_id = data_dict.value
                    else:
                        fields[data_dict.title] = data_dict.value
                    break
        return ref_id, fields
