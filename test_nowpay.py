"""Testing Module"""
from os import getenv

import pytest
from dotenv import load_dotenv
from requests.exceptions import HTTPError

from src.nowpay import NOWPayments

load_dotenv()


@pytest.fixture
def now_pay() -> NOWPayments:
    """
    NOWPayments class fixture.

    :params str api_key: Note, this is not a valid api key, just one that satisfies the regex
    :return: NOWPayments class.
    """
    return NOWPayments(getenv("API_KEY"))


@pytest.fixture
def now_pay_sandbox() -> NOWPayments:
    """
    NOWPayments class fixture.

    :params str api_key: Note, this is not a valid api key, just one that satisfies the regex
    :return: NOWPayments class.
    """
    return NOWPayments(getenv("SANDBOX_API_KEY"), debug_mode=True, sandbox=True)


def test_api_url(now_pay) -> None:
    """
    API url param test

    :param now_pay: NOWPayments class fixture
    :return:
    """
    assert now_pay.api_url == "https://api.nowpayments.io/v1/{}"


def test_sandbox_url(
    now_pay_sandbox: NOWPayments,
) -> None:
    """
    API Sandbox url param test

    :param now_pay: NOWPayments class fixture
    :return:
    """
    assert now_pay_sandbox.api_url == "https://api-sandbox.nowpayments.io/v1/{}"


def test_get_requests(
    now_pay_sandbox: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Get request test
    """
    response = now_pay_sandbox.get("STATUS")
    assert response == "https://api-sandbox.nowpayments.io/v1/status"


def test_api_status(
    now_pay: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Get api status test
    """
    assert now_pay.status() == {"message": "OK"}


def test_currencies(now_pay: NOWPayments) -> None:
    """
    Get available currencies test.
    """
    assert now_pay.currencies().get("currencies", "Not found") != "Not found"


def test_merchant_coins(
    now_pay: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Get available merchant currencies test
    """
    assert (
        now_pay.merchant_coins().get("selectedCurrencies", "Not found") != "Not found"
    )


def test_estimate(now_pay: NOWPayments) -> None:
    """
    Get estimate price test.
    """
    amount = 100
    currency_from = "usd"
    currency_to = "btc"
    result = now_pay.estimate(amount, currency_from, currency_to)
    assert float(result.get("estimated_amount", "Not found")) >= 0.0001
    assert float(result.get("estimated_amount", "Not found")) <= 0.01


def test_estimate_error(now_pay: NOWPayments) -> None:
    """
    Get estimate price test with error.
    """
    amount = 100
    currency_from = "nowpay"
    currency_to = "btc"
    with pytest.raises(HTTPError):
        now_pay.estimate(amount, currency_from, currency_to)


def test_create_payment_unexpected_keyword_argument_error(
    now_pay: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Create payment test with unexpected keyword argument error
    """
    with pytest.raises(TypeError):
        now_pay.create_payment(
            price_amount=100,
            price_currency="usd",
            pay_currency="btc",
            unexpected="argument",
        )


def test_create_payment(now_pay: NOWPayments) -> None:
    """
    Create payment test
    """
    result = now_pay.create_payment(
        price_amount=100, price_currency="usd", pay_currency="btc"
    )
    assert result.get("payment_id", "Not found") != "Not found"


def test_create_payment_with_argument(now_pay: NOWPayments) -> None:
    """
    Create payment test with argument
    """
    result = now_pay.create_payment(
        price_amount=100,
        price_currency="usd",
        pay_currency="btc",
        order_description="My order",
    )
    assert result.get("order_description", "Not found") == "My order"


def test_create_payment_with_error(now_pay: NOWPayments) -> None:
    """
    Create payment test with error
    """

    with pytest.raises(
        HTTPError,
        match="Error 500: This currency is currently unavailable. Try it in 2 hours",
    ):
        now_pay.create_payment(
            price_amount=100, price_currency="usd", pay_currency="cup"
        )


def test_payment_status(now_pay: NOWPayments) -> None:
    """Create payment, then check status is waiting"""
    payment_id = now_pay.create_payment(
        price_amount=100, price_currency="usd", pay_currency="btc"
    )["payment_id"]
    payment = now_pay.payment_status(int(payment_id))
    assert payment["payment_status"] == "waiting", "payment_status"
    assert payment["price_amount"] == 100, "price_amount"
