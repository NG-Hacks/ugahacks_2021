
import requests
import datetime

from const import shared_key, secret_Key, nep_organization, nep_enterprise_unit
from utilities import create_HMAC

content_type = 'application/json'


def bsp_request(url: str, body, method: str):
    date = datetime.datetime.now(datetime.timezone.utc)
    auth = create_HMAC(shared_key,
                       secret_Key,
                       date,
                       method,
                       url,
                       content_type=content_type,
                       nepOrganization=nep_organization)

    headers = {
        'content-type': content_type,
        'Authorization': auth,
        'nep-organization': nep_organization,
        'nep-enterprise-unit': nep_enterprise_unit,
        'date': bytes(date.replace(microsecond=0).strftime('%a, %d %b %Y %H:%M:%S %Z'), 'utf-8')
    }

    if method == 'POST':
        resp = requests.post(url, data=body, headers=headers)
    elif method == 'PATCH':
        resp = requests.patch(url, data=body, headers=headers)
    elif method == 'GET':
        resp = requests.get(url, data=body, headers=headers)
    else:
        return None

    return resp


def bsp_request_comment(url: str, body: str, method: str):
    """
        Used when the request payload should have a key of 'comments'.
    """
    body = {
        'expireAt': '2021-05-08T14:26:48Z',
        'comments': str(body)
    }
    return bsp_request(url, body, method)
