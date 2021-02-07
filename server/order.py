
import json

from bsp import bsp_request
from const import order_service, selling_service


def simulate_order():
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
            "name": "John"
        }
    }
    resp = bsp_request(order_service, json.dumps(body), 'POST')

    if resp.status_code != 200:
        return resp

    return None


def find_order():
    url = f'{order_service}/find'
    body = {
        "pickupContact": {
            "name": "John"
        }
    }
    resp = bsp_request(url, json.dumps(body), 'POST')
    if resp.status_code != 200:
        return resp

    data = resp.json()["pageContent"]

    for d in data:
        try:
            d["referenceId"]
            return None
        except:
            pass

    return 'Did not find a matching order.'
