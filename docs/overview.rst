Getting Started
===============

Installation
------------

``python-allcoin`` is available on `PYPI <https://pypi.python.org/pypi/python-allcoin/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-allcoin


Register on Allcoin
-------------------

Firstly register an account with `Allcoin <https://www.allcoin.com/Account/RegisterByPhoneNumber/?InviteCode=MTQ2OTk4MDgwMDEzNDczMQ==>`_.

Generate an API Key
-------------------

To use signed account methods you are required to verify to create a Transaction Password and then `create an API Key <https://www.allcoin.com/Manage/UserAPI/>`_ and apply appropriate permissions.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from allcoin.client import Client
    client = Client(api_key, api_secret)

API Rate Limit
--------------

Unknown
