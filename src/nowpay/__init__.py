"""
A Python wrapper for the NOWPayments API.
"""

from typing import Any, Dict, Union
from re import match

import requests
from requests import Response
from requests.exceptions import HTTPError


class NOWPayments:
    """
    Class to used for the NOWPayments API.
    """

    debug_mode = False

    key_regex = r"([A-z0-9]{7}-[A-z0-9]{7}-[A-z0-9]{7}-[A-z0-9]{7})"

    # Base URL
    NORMAL_URL = "https://api.nowpayments.io/v1/{}"
    SANDBOX_URL = "https://api-sandbox.nowpayments.io/v1/{}"

    api_url = ""

    endpoints = {
        "STATUS": "status",
        "CURRENCIES": "currencies",
        "MERCHANT_COINS": "merchant/coins",
        "ESTIMATE": "estimate?amount={}&currency_from={}&currency_to={}",
        "PAYMENT": "payment",
        "PAYMENT_STATUS": "payment/{}",
        "MIN_AMOUNT": "min-amount?currency_from={}&currency_to={}",
    }

    def __init__(self, key: str, sandbox: bool = False, debug_mode=False) -> None:
        """
        Class construct. Receives your api key as initial parameter.

        :param str key: API key
        :param bool sandbox: if True, sets api_url to the sandbox url (need sandbox api key)
        :param bool debug_mode: returns the url, instead of doing any requests when successful
        """
        self.debug_mode = debug_mode

        try:
            match(self.key_regex, key).group(0) == key
        except Exception as e:
            raise ValueError("Incorrect API Key format") from e

        self.session = requests.Session()
        self.key = key
        self.headers = {"x-api-key": key, "User-Agent": "nowpay.py"}

        if sandbox:
            self.api_url = self.SANDBOX_URL
        else:
            self.api_url = self.NORMAL_URL

    def create_url(self, endpoint: str) -> str:
        """
        Set the url to be used

        :param str endpoint: Endpoint to be used
        """
        return self.api_url.format(endpoint)

    def get(self, endpoint: str, *args) -> Response:
        """
        Make get requests with your header

        :param str url: URL to which the request is made
        """
        assert endpoint in self.endpoints
        url = self.create_url(self.endpoints[endpoint])
        if len(args) >= 1:
            url = url.format(*args)
        if self.debug_mode:
            return url
        resp = self.session.get(url, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()
        raise HTTPError(
            f'Error {resp.status_code}: {resp.json().get("message", "Not descriptions")}'
        )

    def post(self, endpoint: str, data: Dict) -> Response:
        """
        Make post requests with your header and data

        :param url: URL to which the request is made
        :param data: Data to which the request is made
        """
        assert endpoint in self.endpoints
        url = self.create_url(self.endpoints[endpoint])
        if self.debug_mode:
            return url
        resp = self.session.post(url, data=data, headers=self.headers)
        if resp.status_code in (200, 201):
            return resp.json()
        raise HTTPError(
            f'Error {resp.status_code}: {resp.json().get("message", "Not descriptions")}'
        )

    def status(self) -> Dict:
        """
        This is a method to get information about the current state of the API. If everything
        is OK, you will receive an "OK" message. Otherwise, you'll see some error.
        """
        return self.get("STATUS")

    def currencies(self) -> Dict:
        """
        This is a method for obtaining information about all cryptocurrencies available for
        payments.
        """
        return self.get("CURRENCIES")

    def merchant_coins(self) -> Dict:
        """
        This is a method for obtaining information about the cryptocurrencies available
        for payments. Shows the coins you set as available for payments in the "coins settings"
        tab on your personal account.
        """
        return self.get("MERCHANT_COINS")

    def estimate(
        self, amount: float | int, currency_from: str, currency_to: str
    ) -> Dict:
        """This is a method for calculating the approximate price in cryptocurrency
        for a given value in Fiat currency. You will need to provide the initial cost
        in the Fiat currency (amount, currency_from) and the necessary cryptocurrency
        (currency_to) Currently following fiat currencies are available: usd, eur, nzd,
        brl, gbp.

         :param  float amount: Cost value.
         :param  str currency_from: Fiat currencies.
         :param  str currency_to: Cryptocurrency.
        """
        return self.get("ESTIMATE", amount, currency_from, currency_to)

    def create_payment(
        self,
        price_amount: float | int,
        price_currency: str,
        pay_currency: str,
        **kwargs: Union[str, float, bool, int],
    ) -> Dict:
        """
        With this method, your customer will be able to complete the payment without leaving
        your website.

        :param float price_amount: The fiat equivalent of the price to be paid in crypto.
        :param str price_currency: The fiat currency in which the price_amount is specified.
        :param str pay_currency: The crypto currency in which the pay_amount is specified.
        :param float pay_amount: The amount that users have to pay for the order stated in crypto.
        :param str ipn_callback_url: Url to receive callbacks, should contain "http" or "https".
        :param str order_id: Inner store order ID.
        :param str order_description: Inner store order description.
        :param int purchase_id: Id of purchase for which you want to create a other payment.
        :param str payout_address: Receive funds on another address.
        :param str payout_currency: Currency of your external payout_address.
        :param int payout_extra_id: Extra id or memo or tag for external payout_address.
        :param bool fixed_rate: Required for fixed-rate exchanges.
        :param str case: This only affects sandbox, which status the payment is desired
        """

        data = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            "pay_amount": None,
            "pay_currency": pay_currency,
            "ipn_callback_url": None,
            "order_id": None,
            "order_description": None,
            "buy_id": None,
            "payout_address": None,
            "payout_currency": None,
            "payout_extra_id": None,
            "fixed_rate": None,
            "case": None,
        }
        data.update(**kwargs)
        if len(data) != 13:
            raise TypeError("create_payment() got an unexpected keyword argument")

        return self.post("PAYMENT", data)

    def payment_status(self, payment_id: int) -> Any:
        """
        Get the actual information about the payment.

        :param int payment_id: ID of the payment in the request.
        """
        return self.get("PAYMENT_STATUS", payment_id)

    def min_amount(self, currency_from: str, currency_to: str) -> Any:
        """
        Get the minimum payment amount for a specific pair.

        :param currency_from: Currency from
        :param currency_to: Currency to
        """
        return self.get("MIN_AMOUNT", currency_from, currency_to)
