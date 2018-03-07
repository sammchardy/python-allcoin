# coding=utf-8

import hashlib
import requests
import json
from operator import itemgetter
from .exceptions import AllcoinAPIException, AllcoinRequestException


class Client(object):

    API_URL = 'https://api.allcoin.com/api'
    API_VERSION = 'v1'

    ORDER_STATUS_UNFILLED = 0
    ORDER_STATUS_PARTIALLY_FILLED = 1
    ORDER_STATUS_FILLED = 2
    ORDER_STATUS_CANCELLED = 10

    def __init__(self, api_key, api_secret, requests_params=None):
        """Allcoin API Client constructor

        :param api_key: Api Key
        :type api_key: str.
        :param api_secret: Api Secret
        :type api_secret: str.
        :param requests_params: optional - Dictionary of requests params to use for all calls
        :type requests_params: dict.

        """

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()
        self._requests_params = requests_params

    def _init_session(self):

        session = requests.session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'allcoin/python'})
        return session

    def _create_api_uri(self, path):
        return "{}/{}/{}".format(self.API_URL, self.API_VERSION, path)

    def _generate_signature(self, data):

        ordered_data = self._order_params(data)
        ordered_data.append(('secret_key', self.API_SECRET))
        print("ordered data:{}".format(ordered_data))
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hashlib.md5(query_string.encode('utf-8'))
        return m.hexdigest().upper()

    def _order_params(self, data):
        """Convert params to list with signature as last element

        :param data:
        :return:

        """
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'sign':
                has_signature = True
            else:
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('sign', data['sign']))
        return params

    def _request(self, method, path, signed, **kwargs):

        uri = self._create_api_uri(path)

        # set default requests timeout
        kwargs['timeout'] = 10

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get('data', None)
        if data and isinstance(data, dict):
            kwargs['data'] = data
        if signed:
            # generate signature
            kwargs['data']['api_key'] = self.API_KEY
            kwargs['data']['sign'] = self._generate_signature(kwargs['data'])

        # sort get and post params to match signature order
        if data:
            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del(kwargs['data']['requests_params'])

            # sort post params
            kwargs['data'] = self._order_params(kwargs['data'])

        # if get request assign data array to params value for requests lib
        if data and method == 'get':
            kwargs['params'] = kwargs['data']
            del(kwargs['data'])

        print(kwargs)

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            raise AllcoinAPIException(response)
        try:
            res = response.json()
            if 'error_code' in res:
                raise AllcoinAPIException(response)
            return res
        except ValueError:
            raise AllcoinRequestException('Invalid Response: %s' % response.text)

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request('delete', path, signed, **kwargs)

    # Exchange Endpoints

    def get_ticker(self, symbol):
        """Get the Ticker for the market

        :param symbol: required
        :type symbol: str

        .. code:: python

            ticker = client.get_ticker('eth_btc')

        :returns: API response

        .. code-block:: python

            {
                "date":"1410431279",
                "ticker":{
                    "buy":"33.15",
                    "high":"34.15",
                    "last":"33.15",
                    "low":"32.05",
                    "sell":"33.16",
                    "vol":"10532696.39199642"
                }
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol
        }

        return self._get('ticker', data=params)

    def get_order_book(self, symbol, size=None, merge=None):
        """Get the Order Book for the market

        :param symbol: required
        :type symbol: str
        :param size:  Default 100; max 100
        :type size: int
        :param merge:  merge depth Default 1; max 100
        :type merge: int

        .. code:: python

            # default
            book = client.get_order_book('eth_btc')

            # optional params
            book = client.get_order_book('eth_btc', size=5, merge=5)

        :returns: API response

        .. code-block:: python

            {
                "asks": [
                    [792, 5],
                    [789.68, 0.018],
                    [788.99, 0.042],
                    [788.43, 0.036],
                    [787.27, 0.02]
                ],
                "bids": [
                    [787.1, 0.35],
                    [787, 12.071],
                    [786.5, 0.014],
                    [786.2, 0.38],
                    [786, 3.217],
                    [785.3, 5.322],
                    [785.04, 5.04]
                ]
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol
        }
        if size:
            params['size'] = size
        if merge:
            params['merge'] = merge

        return self._get('depth', data=params)

    def get_trades(self, symbol, since=None):
        """Get the last 600 trades with optional since transaction id parameter

        :param symbol: required
        :type symbol: str
        :param since:  Transaction id (inclusive)
        :type since: int

        .. code:: python

            # default
            trades = client.get_trades('eth_btc')

            # default
            trades = client.get_trades('eth_btc', since=230433)

        :returns: API response

        .. code-block:: python

            [
                {
                    "date": "1367130137",
                    "date_ms": "1367130137000",
                    "price": 787.71,
                    "amount": 0.003,
                    "tid": "230433",
                    "type": "sell"
                },
                {
                    "date": "1367130137",
                    "date_ms": "1367130137000",
                    "price": 787.65,
                    "amount": 0.001,
                    "tid": "230434",
                    "type": "sell"
                },
                {
                    "date": "1367130137",
                    "date_ms": "1367130137000",
                    "price": 787.5,
                    "amount": 0.091,
                    "tid": "230435",
                    "type": "sell"
                }
            ]

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol
        }
        if since:
            params['since'] = since

        return self._get('trades', data=params)

    def get_trade_history(self, symbol, since=None):
        """Get trade history - requires api key

        :param symbol: required
        :type symbol: str
        :param since:  Transaction id (inclusive)
        :type since: int

        .. code:: python

            # default
            trades = client.get_trade_history('eth_btc')

            # default
            trades = client.get_trade_history('eth_btc', since=230433)

        :returns: API response

        .. code-block:: python

            [
                {
                    "date": 1367130137,
                    "date_ms": 1367130137000,
                    "price": 787.71,
                    "amount": 0.003,
                    "tid": "230433",
                    "type": "sell"
                },
                {
                    "date": 1367130137,
                    "date_ms": 1367130137000,
                    "price": 787.65,
                    "amount": 0.001,
                    "tid": "230434",
                    "type": "sell"
                },
                {
                    "date": 1367130137,
                    "date_ms": 1367130137000,
                    "price": 787.5,
                    "amount": 0.091,
                    "tid": "230435",
                    "type": "sell"
                }
            ]

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol
        }
        if since:
            params['since'] = since

        return self._post('trade_history', data=params, signed=True)

    def get_klines(self, symbol, kline_type, size=None, since=None):
        """Get klines for a symbol

        :param symbol: required
        :type symbol: str
        :param kline_type:  type of candlestick (1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 12hour, 1day, 3day, 1week)
        :type kline_type: str
        :param size: number of klines to return
        :type size: int
        :param since: timestamp in ms to return from
        :type since: int

        .. code:: python

            # default
            klines = client.get_klines('eth_btc', '1min')

            # optional params
            klines = client.get_klines('eth_btc', '1hour', size=20, since=1417449600000)

        :returns: API response

        .. code-block:: python

            [
                [
                    1417449600000,  # timestamp
                    2339.11,        # open
                    2383.15,        # high
                    2322,           # low
                    2369.85,        # close
                    83850.06        # volume
                ],
                [
                    1417536000000,
                    2370.16,
                    2380,
                    2352,
                    2367.37,
                    17259.83
                ]
            ]

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'type': kline_type
        }
        if size:
            params['size'] = size
        if since:
            params['since'] = since

        return self._get('kline', data=params)

    # User information

    def get_userinfo(self):
        """Get account info

        .. code:: python

            # default
            info = client.get_userinfo()

        :returns: API response

        .. code-block:: python

            {
                "info": {
                    "funds": {
                        "free": {
                            "btc": "0",
                            "usd": "0",
                            "ltc": "0"
                        },
                        "freezed": {
                            "btc": "0",
                            "usd": "0",
                            "ltc": "0"
                        }
                    }
                },
                "result": true
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {}

        return self._post('userinfo', data=params, signed=True)

    # Trading Endpoints

    def create_order(self, symbol, side, price, amount):
        """Create an order

        :param symbol: required
        :type symbol: str
        :param side:  order side buy/sell
        :type side: str
        :param price: order price
        :type price: str
        :param amount: order quantity
        :type amount: str

        .. code-block:: python

            # default
            order = client.create_order('eth_btc', 'buy', '0.2348', '100')

        :returns: API response

        .. code-block:: python

            {
                "order_id": "123456",
                "result": true
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'type': side,
            'price': price,
            'amount': amount,
        }

        return self._post('trade', data=params, signed=True)

    def create_buy_order(self, symbol, price, amount):
        """Create a buy order

        :param symbol: required
        :type symbol: str
        :param price: order price
        :type price: str
        :param amount: order quantity
        :type amount: str

        .. code-block:: python

            # default
            order = client.create_buy_order('eth_btc', '0.2348', '100')

        :returns: API response

        .. code-block:: python

            {
                "order_id": "123456",
                "result": true
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """

        return self.create_order(symbol, 'buy', price, amount)

    def create_sell_order(self, symbol, price, amount):
        """Create a sell order

        :param symbol: required
        :type symbol: str
        :param price: order price
        :type price: str
        :param amount: order quantity
        :type amount: str

        .. code-block:: python

            # default
            order = client.create_buy_order('eth_btc', '0.2348', '100')

        :returns: API response

        .. code-block:: python

            {
                "order_id": "123456",
                "result": true
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """

        return self.create_order(symbol, 'sell', price, amount)

    def batch_orders(self, symbol, order_data, order_type=None):
        """Create an order

        :param symbol: required
        :type symbol: str
        :param order_data: list of dictionaries of price, amount and type
        :type order_data: list of dicts
        :param order_type: optional buy/sell default used if type not set in order_data dict
        :type order_type: str

        .. code-block:: python

            order_data = [
                {
                    "price": "0.0123",
                    "amount": "120",
                    "type": "sell"
                },
                {
                    "price": "0.0112",
                    "amount": "110"
                }
            ]
            order = client.create_order('eth_btc', order_data, type='buy')

        :returns: API response

        .. code-block:: python

            {
                "order_info":[
                    {"order_id":41724206},
                    {"error_code":10011,"order_id":-1},
                    {"error_code":10014,"order_id":-1}
                ],
                "result":true
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'order_data': json.dumps(order_data, separators=(',', ':'))
        }
        if order_type:
            params['type'] = order_type

        return self._post('batch_trade', data=params, signed=True)

    def cancel_order(self, symbol, order_id):
        """Cancel an order or up to 3 orders

        :param symbol: required
        :type symbol: str
        :param order_id: order ID (multiple orders are separated by a comma ',', 3 orders at most are allowed per request)
        :type order_id: str

        .. code-block:: python

            # single order
            order = client.cancel_order('eth_btc', '123456')

            # multiple orders
            order = client.cancel_order('eth_btc', '123456,123457,123557')

        :returns: API response

        .. code-block:: python

            # single order id
            {
                "order_id": "123456",
                "result": true
            }

            # multiple order ids
            {
                "success":"123456,123457",
                "error":"123458"
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'order_id': order_id
        }

        return self._post('cancel_order', data=params, signed=True)

    def get_order(self, symbol, order_id):
        """Get info about a particular order

        :param symbol: required
        :type symbol: str
        :param order_id: order ID to fetch
        :type order_id: str

        .. code-block:: python

            order = client.get_order('eth_btc', '123456')

        :returns: API response

        .. code-block:: python

            {
                "result": true,
                "orders": [
                    {
                        "amount": 0.1,
                        "avg_price": 0,                 # average transaction price
                        "create_date": 1418008467000,   # order time
                        "deal_amount": 0,               # filled quantity
                        "order_id": 10000591,           # order id
                        "price": 500,                   # entrustment price
                        "status": 0,                    # 0 = unfilled, 1 = partially filled, 2 = fully filled, 10 = cancelled
                        "symbol": "btc_usd",
                        "type": "sell"
                    },
                    {
                        "amount": 0.2,
                        "avg_price": 0,
                        "create_date": 1417417957000,
                        "deal_amount": 0,
                        "order_id": 10000724,
                        "price": 0.1,
                        "status": 0,
                        "symbol": "btc_usd",
                        "type": "buy"
                    }
                ]
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'order_id': order_id
        }

        return self._post('order_info', data=params, signed=True)

    def get_open_orders(self, symbol):
        """Get info about all open orders

        :param symbol: required
        :type symbol: str

        .. code-block:: python

            order = client.get_open_orders('eth_btc')

        :returns: API response

        .. code-block:: python

            {
                "result": true,
                "orders": [
                    {
                        "amount": 0.1,
                        "avg_price": 0,                 # average transaction price
                        "create_date": 1418008467000,   # order time
                        "deal_amount": 0,               # filled quantity
                        "order_id": 10000591,           # order id
                        "price": 500,                   # entrustment price
                        "status": 0,                    # 0 = unfilled, 1 = partially filled, 2 = fully filled, 10 = cancelled
                        "symbol": "btc_usd",
                        "type": "sell"
                    },
                    {
                        "amount": 0.2,
                        "avg_price": 0,
                        "create_date": 1417417957000,
                        "deal_amount": 0,
                        "order_id": 10000724,
                        "price": 0.1,
                        "status": 0,
                        "symbol": "btc_usd",
                        "type": "buy"
                    }
                ]
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """

        return self.get_order(symbol, order_id="-1")

    def get_orders(self, symbol, order_status, order_ids):
        """Get info about multiple orders

        :param symbol: required
        :type symbol: str
        :param order_status: 0 for unfilled orders; 1 for filled orders
        :type order_status: int
        :param order_ids: order IDs to fetch (multiple orders are separated by ',', 50 orders at most are allowed per request)
        :type order_ids: str

        .. code-block:: python

            order = client.get_orders('eth_btc', 1)

        :returns: API response

        .. code-block:: python

            {
                "result": true,
                "orders": [
                    {
                        "amount": 0.1,
                        "avg_price": 0,                 # average transaction price
                        "create_date": 1418008467000,   # order time
                        "deal_amount": 0,               # filled quantity
                        "order_id": 10000591,           # order id
                        "price": 500,                   # entrustment price
                        "status": 0,                    # 0 = unfilled, 1 = partially filled, 2 = fully filled, 10 = cancelled
                        "symbol": "btc_usd",
                        "type": "sell"
                    },
                    {
                        "amount": 0.2,
                        "avg_price": 0,
                        "create_date": 1417417957000,
                        "deal_amount": 0,
                        "order_id": 10000724,
                        "price": 0.1,
                        "status": 0,
                        "symbol": "btc_usd",
                        "type": "buy"
                    }
                ]
            }

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'type': order_status,
            'order_id': order_ids
        }

        return self._post('orders_info', data=params, signed=True)

    def get_order_history(self, symbol, order_status, page=1, limit=200):
        """Get history of orders for a symbol

        :param symbol: required
        :type symbol: str
        :param order_status: 0 for unfilled orders; 1 for filled orders
        :type order_status: int
        :param page: page to fetch
        :type page: int
        :param limit: amount on each page
        :type limit: int

        .. code-block:: python

            order = client.get_order_history('eth_btc', 1)

        :returns: API response

        .. code-block:: python

            [
                {
                    "current_page": 1,
                    "orders": [
                        {
                            "amount": 0,
                            "avg_price": 0,
                            "create_date": 1405562100000,
                            "deal_amount": 0,
                            "order_id": 0,
                            "price": 0,
                            "status": 2,
                            "symbol": "btc_usd",
                            "type": "sell”
                        }
                    ],
                    "page_length": 1,
                    "result": true,
                    "total": 3
                }
            ]

        :raises: AllcoinResponseException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'status': order_status,
            'current_page': page,
            'page_length': limit
        }

        return self._post('order_history', data=params, signed=True)
