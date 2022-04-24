# NowPay-Python

[![CodeQL](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/codeql-analysis.yml)
[![Pylint](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/pylint.yml/badge.svg)](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/pylint.yml)
[![Python application](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/python-app.yml/badge.svg)](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/python-app.yml)
[![Upload Python Package](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/python-publish.yml/badge.svg)](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/python-publish.yml)
[![codecov](https://codecov.io/gh/NikolaiSch/NowPay-Python/branch/main/graph/badge.svg?token=Z7NIDJI2LD)](https://codecov.io/gh/NikolaiSch/NowPay-Python)
[![Black](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/black.yml/badge.svg)](https://github.com/NikolaiSch/NowPay-Python/actions/workflows/black.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repo is for the python package called __"nowpay"__

A Python wrapper for the [NOWPayments API](https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest).  

The api call descriptions are from the official documentation.

## Getting Started

Before using the NOWPayments API, sign up for a [API key here](https://nowpayments.io/).

If you want to use the Sandbox, request your [API key here](https://account-sandbox.nowpayments.io/).

To install the wrapper, enter the following into the terminal.

```bash
pip install nowpay
```

Every api call requires this api key. Make sure to use this key when getting started.

```python
from nowpay import NOWPayments

now_pay = NOWPayments(API_KEY)

status = now_pay.status()
```

Sandbox is used in the same way in correspondence with the documentation as follows.

```python
from nowpay import NOWPayments

now_pay = NOWPayments(SANDBOX_API_KEY, True)

status = now_pay.status()
```

How to use the IPN  

export_app() returns a WSGI app that can be hosted with waitress, gurnicorn or others

```python
from nowpay.ipn import Ipn

def success(dictionary):
  print(dictionary)

ipn = Ipn("My_IPN_Secret", success)
app = ipn.export_app()

app.run()
```

## Breaking Changes from 1.1.1

- Renamed Function names
  - status (for api status)
  - currencies (for all available currencies)
  - merchant_coins (for your account allowed coins)
  - estimate (to estimate cost for a transaction)
  - create_payment (to create a payment transaction, returns details)
  - payment_status (to view payment status from id)
  - min_amount (view minimum cost of a transaction allowed from 1 crypto to another)
- No more extra sandbox class (built in)
  - Now use sandbox=True in the constructor
  - added case support, now in sandbox mode, you are able to specify case.
    - valid cases are "success", "partially_paid", "failure" to test your api

### Credit

Originally written by _[@Ventura94](https://github.com/Ventura94)_
