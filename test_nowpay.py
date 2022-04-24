"""Testing Module"""
from os import getenv
from dotenv import load_dotenv
from typing import Any, Dict, Union
import pytest
from pytest_mock.plugin import MockerFixture
from requests.exceptions import HTTPError
from src.nowpay import NOWPayments

load_dotenv()


@pytest.fixture
def np() -> NOWPayments:
    """
    NOWPayments class fixture.

    :params str api_key: Note, this is not a valid api key, just one that satisfies the regex: \w{7}-\w{7}-\w{7}-\w{7}
    :return: NOWPayments class.
    """
    return NOWPayments(getenv("API_KEY"))


@pytest.fixture
def np_sandbox() -> NOWPayments:
    """
    NOWPayments class fixture.

    :params str api_key: Note, this is not a valid api key, just one that satisfies the regex: \w{7}-\w{7}-\w{7}-\w{7}
    :return: NOWPayments class.
    """
    return NOWPayments(getenv("SANDBOX_API_KEY"), debug_mode=True, sandbox=True)


def test_api_url(np) -> None:
    """
    API url param test

    :param np: NOWPayments class fixture
    :return:
    """
    assert np.API_URL == "https://api.nowpayments.io/v1/{}"


def test_sandbox_url(
    np_sandbox: NOWPayments,
) -> None:
    """
    API Sandbox url param test

    :param np: NOWPayments class fixture
    :return:
    """
    assert np_sandbox.API_URL == "https://api-sandbox.nowpayments.io/v1/{}"


def test_get_requests(
    np_sandbox: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Get request test
    """
    response = np_sandbox.GET("STATUS")
    assert response == "https://api-sandbox.nowpayments.io/v1/status"


def test_api_status(
    np: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Get api status test
    """
    assert np.status() == {"message": "OK"}


def test_currencies(np: NOWPayments) -> None:
    """
    Get available currencies test.
    """
    assert np.currencies().get("currencies", "Not found") != "Not found"


def test_merchant_coins(
    np: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Get available merchant currencies test
    """
    assert np.merchant_coins().get("selectedCurrencies", "Not found") != "Not found"


def test_estimate(np: NOWPayments) -> None:
    """
    Get estimate price test.
    """
    amount = 100
    currency_from = "usd"
    currency_to = "btc"
    result = np.estimate(amount, currency_from, currency_to)
    assert float(result.get("estimated_amount", "Not found")) >= 0.0001
    assert float(result.get("estimated_amount", "Not found")) <= 0.01


def test_estimate_error(np: NOWPayments) -> None:
    """
    Get estimate price test with error.
    """
    amount = 100
    currency_from = "nowpay"
    currency_to = "btc"
    with pytest.raises(HTTPError):
        np.estimate(amount, currency_from, currency_to)


def test_create_payment_unexpected_keyword_argument_error(
    np: NOWPayments,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Create payment test with unexpected keyword argument error
    """
    with pytest.raises(TypeError):
        np.create_payment(
            price_amount=100,
            price_currency="usd",
            pay_currency="btc",
            unexpected="argument",
        )


def test_create_payment(np: NOWPayments) -> None:
    """
    Create payment test
    """
    result = np.create_payment(
        price_amount=100, price_currency="usd", pay_currency="btc"
    )
    assert result.get("payment_id", "Not found") != "Not found"


def test_create_payment_with_argument(np: NOWPayments) -> None:
    """
    Create payment test with argument
    """
    result = np.create_payment(
        price_amount=100,
        price_currency="usd",
        pay_currency="btc",
        order_description="My order",
    )
    assert result.get("order_description", "Not found") == "My order"


def test_create_payment_with_error(np: NOWPayments) -> None:
    """
    Create payment test with error
    """

    with pytest.raises(
        HTTPError,
        match="Error 500: This currency is currently unavailable. Try it in 2 hours",
    ):
        np.create_payment(price_amount=100, price_currency="usd", pay_currency="cup")


def test_payment_status(np: NOWPayments) -> None:
    """Create payment, then check status is waiting"""
    payment_id = np.create_payment(
        price_amount=100, price_currency="usd", pay_currency="btc"
    )["payment_id"]
    p = np.payment_status(int(payment_id))
    assert p["payment_status"] == "waiting", "payment_status"
    assert p["price_amount"] == 100, "price_amount"
