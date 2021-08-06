import json
from flask import request, Response

from services import app
from utils.attr_dict import AttrDict
from webhooks.crud import Webhook
from webhooks.model import CrudRequest

webhook_obj = Webhook()


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/api/push_data', methods=['POST'])
def push_data():
    try:
        # Getting Json from request object
        req_json = request.get_json()
        print(f'webhook request: [{req_json}]')

        config_file = open('./config.json')
        config_json = json.load(config_file)
        print(f'config json: [{config_json}]')

        # Loading and Validating Json objects from request
        req = CrudRequest.load_json(req_json)

        # Converting Json object to dictionary mapping, so can easily accessible by using with '.'
        req_webhook = AttrDict(req.webhook)
        config = AttrDict(config_json)

        airtable_api_key = config.airtable_api_key
        for form in config.forms:
            form_dict = AttrDict(form)

            # Checking which function to call either create or update
            if form_dict.form_id == req_webhook.form_id:
                if form_dict.action == 'create':
                    result = webhook_obj.create(airtable_api_key, form_dict, req_webhook)
                elif form_dict.action == 'update':
                    result = webhook_obj.update(airtable_api_key, form_dict, req_webhook)
                break
        return result
    except KeyError as exp:
        print(f'Key not found: {str(exp)}')
        return 'Key not found:' + str(exp)
    except Exception as exp:
        print(f'{str(exp)}')
        return str(exp)
