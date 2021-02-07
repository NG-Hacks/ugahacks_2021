
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
    resp = simulate_order()

    if resp is not None:
        err = app.response_class(
            response=f"Error {resp.text}.",
            status=400,
            mimetype=content_type
        )
        return err

    return app.response_class(
        response="Success.",
        status=200,
        mimetype=content_type
    )


@app.route('/orders/find', methods=['POST'])
def retrieve_order():
    """
        POST: find an order with matching nanme 
    """
    resp = find_order()

    if resp is not None:
        if isinstance(resp, requests.Respone):
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
