from typing import Any


class CrudRequest:

    def __init__(self, webhook: Any):
        # self.config = config
        self.webhook = webhook

    @staticmethod
    def load_json(json: Any) -> 'CrudRequest':
        if not json:
            raise Exception("Invalid request.")
        # if 'config' not in json:
        #     raise Exception("config json not found.")
        # if 'data' not in json:
        #     raise Exception("data json not found.")
        return CrudRequest(json)
