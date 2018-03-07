================================
Welcome to python-allcoin v0.0.1
================================

.. image:: https://img.shields.io/pypi/v/python-allcoin.svg
    :target: https://pypi.python.org/pypi/python-allcoin

.. image:: https://img.shields.io/pypi/l/python-allcoin.svg
    :target: https://pypi.python.org/pypi/python-allcoin

.. image:: https://img.shields.io/travis/sammchardy/python-allcoin.svg
    :target: https://travis-ci.org/sammchardy/python-allcoin

.. image:: https://img.shields.io/coveralls/sammchardy/python-allcoin.svg
    :target: https://coveralls.io/github/sammchardy/python-allcoin

.. image:: https://img.shields.io/pypi/wheel/python-allcoin.svg
    :target: https://pypi.python.org/pypi/python-allcoin

.. image:: https://img.shields.io/pypi/pyversions/python-allcoin.svg
    :target: https://pypi.python.org/pypi/python-allcoin

This is an unofficial Python wrapper for the `Allcoin exchanges REST API v1 <https://www.allcoin.com/About/API/>`_. I am in no way affiliated with Allcoin, use at your own risk.

PyPi
  https://pypi.python.org/pypi/python-allcoin

Source code
  https://github.com/sammchardy/python-allcoin

Documentation
  https://python-allcoin.readthedocs.io/en/latest/

Blog with examples
  https://sammchardy.github.io


Features
--------

- Implementation of all REST endpoints
- Simple handling of authentication
- Response exception handling

Quick Start
-----------

Register an account with `Allcoin <https://www.allcoin.com/Account/RegisterByPhoneNumber/?InviteCode=MTQ2OTk4MDgwMDEzNDczMQ==>`_.

To use signed account methods you are required to verify to create a Transaction Password and then `create an API Key <https://www.allcoin.com/Manage/UserAPI/>`_ and apply appropriate permissions.

.. code:: bash

    pip install python-allcoin


.. code:: python

    from allcoin.client import Client
    client = Client(api_key, api_secret)

    # get market depth
    depth = client.get_order_book('eth_btc', size=50)

    # get symbol klines
    klines = client.get_klines('eth_btc', '1day')

    # place a buy order
    transaction = client.create_buy_order('eth_btc', '0.01', '1000')

    # get list of open orders
    orders = client.get_open_orders('eth_btc')

    # cancel an order
    orders = client.cancel_order('eth_btc', '1235')

    # get order info
    orders = client.get_order('eth_btc', '1235')


For more `check out the documentation <https://python-allcoin.readthedocs.io/en/latest/>`_.

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance <https://www.binance.com/?ref=10099792>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.

If you use `Kucoin <https://www.kucoin.com/#/?r=E42cWB>`_ check out my `python-kucoin <https://github.com/sammchardy/python-kucoin>`_ library.

If you use `Quoinex <https://accounts.quoinex.com/sign-up?affiliate=PAxghztC67615>`_
or `Qryptos <https://accounts.qryptos.com/sign-up?affiliate=PAxghztC67615>`_ check out my `python-quoine <https://github.com/sammchardy/python-quoine>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

If you use `BigONE <https://big.one>`_ check out my `python-bigone <https://github.com/sammchardy/python-bigone>`_ library.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-allcoin?pixel