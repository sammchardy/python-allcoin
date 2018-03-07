Exceptions
==========

AllcoinResponseException
-----------------------

Raised if a non JSON response is returned

AllcoinAPIException
------------------

On an API call error a allcoin.exceptions.AllcoinAPIException will be raised.

The exception provides access to the

- `status_code` - response status code
- `response` - response object
- `code` - Allcoin error code
- `message` - Allcoin error message
- `request` - request object if available

.. code:: python

    try:
        client.get_ticker('eth_btc')
    except AllcoinAPIException as e:
        print(e.status_code)
        print(e.code)
        print(e.message)
