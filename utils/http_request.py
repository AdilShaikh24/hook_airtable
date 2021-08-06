import requests


def make_http_get_request(url, headers):
    resp = requests.get(url, headers=headers)
    return resp


def make_http_post_request(url, data, headers):
    resp = requests.post(url, data=data, headers=headers)
    return resp


def make_http_patch_request(url, data, headers):
    resp = requests.patch(url, data=data, headers=headers)
    return resp
