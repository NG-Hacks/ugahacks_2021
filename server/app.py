
import json

from flask import Flask, request
import requests

from order import simulate_order, find_order


app = Flask(__name__)
content_type = 'application/json'


# ORDERS

@app.route('/orders', methods=['POST'])
def create_order():
    """
        POST: create a simulated cart and order
    """
    data = request.get_json()
    name = data.get('name', None)

    resp = simulate_order(name)

    if isinstance(resp, requests.Response):
        err = app.response_class(
            response=f"Error {resp.text}.",
            status=400,
            mimetype=content_type
        )
        return err

    return app.response_class(
        response=json.dumps({"Code": "Success."}),
        status=200,
        mimetype=content_type
    )


@ app.route('/orders/find', methods=['POST'])
def retrieve_order():
    """
        POST: find an order with matching nanme
    """
    data = request.get_json()
    name = data.get('name', None)
    reference_id = data.get('referenceId', None)

    resp = find_order(name, reference_id)

    if resp is not None:
        if isinstance(resp, requests.Response):
            err = app.response_class(
                response=f"Error {resp.text}.",
                status=400,
                mimetype=content_type
            )
            return err
        else:
            err = app.response_class(
                response=resp,
                status=400,
                mimetype=content_type
            )
            return err

    return app.response_class(
        response="Success.",
        status=200,
        mimetype=content_type
    )


if __name__ == '__main__':
    app.run()
