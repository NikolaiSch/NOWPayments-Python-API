"""
A Python premade ipn setup for NOWPayments
"""
from typing import Dict
from flask import Flask, request
import json
import hashlib
import hmac


class Ipn:
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def ipn(self):
        data = request.json
        sig = request.headers["x-nowpayments-sig"]
        if sig == self.hmac_sign(data):
            self.success(data)

    def __init__(self, secret: str, success):
        self.secret = bytes(secret, "utf8")
        self.success = success

    def hmac_sign(self, response: Dict) -> str:
        to_hash = bytes(json.dumps(dict(sorted(response.items()))), "utf8")
        return hmac.new(self.secret, to_hash, hashlib.sha512).hexdigest()

    def export_app(self):
        return self.app
