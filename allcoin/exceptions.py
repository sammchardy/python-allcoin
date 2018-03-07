# coding=utf-8


class AllcoinAPIException(Exception):

    CODES = {
        "10000": "Required field, can not be null",
        "10001": "Request too frequently",
        "10002": "System error",
        "10006": "User doesn't exist",
        "10007": "Signature does not match",
        "10008": "Illegal parameter",
        "10009": "Order does not exist",
        "10010": "Insufficient funds",
        "10012": "Only support https request",
        "10013": "Order price is out of range",
        "10014": "Insufficient coins quantity",
        "10016": "Failed to get latest transaction price",
        "10017": "The specified currency does not exist",
        "10018": "Out of the valid trading time",
        "10019": "Blacklist user",
        "10022": "Trading zone is closed",
        "10023": "Order quantity is out of the time limit",
        "10025": "Wrong order number",
        "10026": "Fail to get the info of the trading zone",
        "10027": "Your order is revoked, please do not repeat the operation",
        "10028": "The order has been completed and cannot be cancelled",
        "10029": "Users are not authorized to do the operation",
        "10030": "System is under maintaince",
        "10031": "The price has exceeded the daily limitation.",
        "10032": "The currency purchase has been suspended.",
        "10033": "The currency sale has been suspended.",
        "10034": "Pass KYC level 1 to continue"
    }

    def __init__(self, response):
        self.status_code = 0
        self.message = "Unknown Error"
        self.code = ""
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Allcoin: {}'.format(response.text)
        else:
            self.code = json_res['error_code']
        try:
            self.message = self.CODES[self.code]
        except KeyError:
            pass
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'AllcoinAPIException(code=%s): %s' % (self.code, self.message)


class AllcoinRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'AllcoinRequestException: %s' % self.message
