from typing import Dict
from nowpay.ipn import Ipn
from waitress import serve


def success(request: Dict) -> None:
    """Callback function on ipn successful verification of signature header

    standard steps:
    1) create a payment with nowpayments.NOWPayments, with order_id, related to an order or a user for use on success
    2) check if request["payment_status"] == "finished"
        3a) if not, return
        3b) if it is, do something, such as updating database

    :param Dict request: contains a response body like the following:
    {"payment_id":5077125051,
    "payment_status":"waiting",
    "pay_address":"0xd1cDE08A07cD25adEbEd35c3867a59228C09B606",
    "price_amount":170,
    "price_currency":"usd",
    "pay_amount":155.38559757,
    "actually_paid":0,
    "pay_currency":"mana",
    "order_id":"2",
    "order_description":"Apple Macbook Pro 2019 x 1",
    "purchase_id":"6084744717",
    "created_at":"2021-04-12T14:22:54.942Z",
    "updated_at":"2021-04-12T14:23:06.244Z",
    "outcome_amount":1131.7812095,
    "outcome_currency":"trx"}
    """

    if request["payment_status"] == "finished":
        # We now add balance to the user or add the order todo
        print(request["order_id"])


my_ipn = Ipn("my_secret", success)

app = my_ipn.export_app()


# Now we can serve our app with a production wsgi server such as waitress

serve(app, host="0.0.0.0", port="8000")
