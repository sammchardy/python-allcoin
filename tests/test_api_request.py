#!/usr/bin/env python
# coding=utf-8

from allcoin.client import Client
from allcoin.exceptions import AllcoinAPIException, AllcoinRequestException
import pytest
import requests_mock


client = Client('api_key', 'api_secret')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(AllcoinRequestException):
        with requests_mock.mock() as m:
            m.get('https://api.allcoin.com/api/v1/depth?symbol=eth_btc', text='<head></html>')
            client.get_order_book(symbol='eth_btc')


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(AllcoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                "error_code": "10017",
                "result": False
            }
            m.get('https://api.allcoin.com/api/v1/depth?symbol=eth_btc', json=json_obj, status_code=200)
            client.get_order_book(symbol='eth_btc')
