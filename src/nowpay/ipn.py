"""
A Python premade ipn setup for NOWPayments
"""
import hashlib
import hmac
import json
from typing import Dict

from flask import Flask, request


class Ipn:
    """This is a class for the IPN that can be used to create a quick IPN web server using flask"""

    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def ipn(self):
        """Handles all post requests, for the ipn, then calls success"""
        data = request.json
        sig = request.headers["x-nowpayments-sig"]
        if sig == self.hmac_sign(data):
            self.success(data)

    def __init__(self, secret: str, success):
        """Supply the secret and success function"""
        self.secret = bytes(secret, "utf8")
        self.success = success

    def hmac_sign(self, response: Dict) -> str:
        """An internal function for verifying the hmac signature"""
        to_hash = bytes(json.dumps(dict(sorted(response.items()))), "utf8")
        return hmac.new(self.secret, to_hash, hashlib.sha512).hexdigest()

    def export_app(self):
        """This function exports the flask app created"""
        return self.app
