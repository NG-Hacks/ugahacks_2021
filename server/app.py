
import requests
import datetime
import json

from flask import Flask, request

from const import shared_key, secret_Key, nep_organization, nep_enterprise_unit
from utilities import create_HMAC

app = Flask(__name__)

# URLS
order_service = 'urlhere'


def bsp_request(url: str, body, method: str):
    date = datetime.datetime.now(datetime.timezone.utc)
    content_type = 'application/json'

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

    resp = requests.post(url, data=json.dumps(body), headers=headers)

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


# ORDERS

@app.route("/orders", methods=["POST"])
def create_order():
    """
        POST: create an order
    """
    if request.method == 'POST':
        url = order_service
        response = bsp_request_comment(url, request.data, request.method)
        return response.text


@app.route("/orders/find", methods=["POST"])
def find_order():
    """
        POST: find an order
    """
    if request.method == 'POST':
        url = f'{order_service}/find'
        response = bsp_request(url, request.data, request.method)
        return response.text


@app.route("/orders/<order_id>", methods=["GET", "PUT"])
def orders_id(order_id):
    """
        GET: get an order by ID
        PUT: replace an order
    """
    if request.method in ['GET', 'PUT']:
        url = f'{order_service}/{order_id}'
        response = bsp_request(url, request.data, request.method)
        return response.text
