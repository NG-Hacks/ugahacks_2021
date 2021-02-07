
import json

from bsp import bsp_request, bsp_request_param
from const import order_service, selling_service


def simulate_order(name):
    # 1. POST create cart
    resp = bsp_request(selling_service, "{}", 'POST')
    cart_id = resp.headers['Location'].split('/')[2]

    # 2. POST add item to cart
    cart_url = f'{selling_service}/{cart_id}'
    body = {
        "scanData": "101",
        "quantity": {
            "unitOfMeasure": "EA",
            "value": 1
        }
    }
    resp = bsp_request(f'{cart_url}/items', json.dumps(body), 'POST')
    print(f'Add item to cart: {resp.status_code}')
    if resp.status_code != 201:
        return resp

    # 3. PATCH update cart status total
    body = {
        "status": "Total"
    }
    resp = bsp_request(cart_url, json.dumps(body), 'PATCH')
    print(f'Update cart status to Total: {resp.status_code}')
    if resp.status_code != 200:
        return resp

    # 4. PATCH update cart status tender
    body = {
        "status": "Tender"
    }
    resp = bsp_request(cart_url, json.dumps(body), 'PATCH')
    print(f'Update cart status to Tender: {resp.status_code}')
    if resp.status_code != 200:
        return resp

    # 5.GET cart before payment
    resp = bsp_request(cart_url, "{}", 'GET')
    print(f'Get cart before payment: {resp.status_code}')
    if resp.status_code != 200:
        return resp

    balance_due = resp.json()["totals"]["balanceDue"]
    print(f'Balance due: {balance_due}')

    # 6.POST add tender
    body = {
        "tenderId": "2",
        "amount": float(balance_due),
        "status": "authorized",
        "authorization": {
            "authorizationType": "local",
            "authorizationCode": "OK200",
            "referenceNumber": "36787687687"
        }
    }
    resp = bsp_request(cart_url + "/tenders", json.dumps(body), 'POST')
    print(f'Add tender: {resp.status_code}')
    if resp.status_code != 201:
        return resp

    # 7.PATCH update cart status Finalization
    body = {
        "status": "Finalization"
    }

    resp = bsp_request(cart_url, json.dumps(body), 'PATCH')
    print(f'Update cart status to Finalization: {resp.status_code}')
    if resp.status_code != 200:
        return resp

    # 8.PATCH update cart status Closed
    body = {
        "status": "Closed"
    }
    resp = bsp_request(cart_url, json.dumps(body), 'PATCH')
    print(f'Update cart status to Closed: {resp.status_code}')
    if resp.status_code != 200:
        return resp

    # 9.POST create order
    body = {
        "expireAt": "2020-05-08T14:26:48Z",
        "comments": "Good-Morning",
        "referenceID": cart_id,
        "pickupContact": {
            "name": f"{name}"
        }
    }
    resp = bsp_request(order_service, json.dumps(body), 'POST')
    print(resp.json())

    if resp.status_code != 200:
        return resp

    return None


def find_order(name=None, reference_id=None):
    url = f'{order_service}/find?pageSize=1000'
    # url = f'{order_service}/find'

    if not name:
        return "You must specify customer name."

    resp = bsp_request(url, "{}", 'POST')
    if resp.status_code != 200:
        return resp

    data = resp.json()["pageContent"]

    for d in data:
        try:
            order_id = d['id']
            order_url = f'{order_service}/{order_id}'
            resp = bsp_request(order_url, {}, 'GET')
            print(resp.status_code)
            print(resp.json())

            # check if order matches name
            if resp.json()["pickupContact"]["name"] != name:
                raise ValueError

            # check if order has a reference id
            d["referenceId"]
            return None
        except:
            pass

    return json.dumps({'Error:': 'Did not find a matching order.'})
