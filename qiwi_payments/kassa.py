import json
import uuid
import datetime as dt
from decimal import Decimal

import pytz

from qiwi_payments.utils import HttpClient
from qiwi_payments.models import Invoice, Refund


class QiwiKassa:
    def __init__(self, secret_key: str):
        self._secret_key = secret_key
        self.api = HttpClient()
        self.base_url = 'https://api.qiwi.com/partner/bill/v1/bills/'

    @property
    def headers(self) -> dict:
        return {
            'Authorization': 'Bearer {}'.format(self._secret_key),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def create_bill(
            self,
            amount: Decimal,
            currency: str = 'RUB',
            comment: str = '',
            expire_in: dt.timedelta = dt.timedelta(days=1),
            email: str = '',
            timezone: str = 'Europe/Moscow') -> Invoice:
        """
        :param amount: amount value
        :param currency: ISO code of currency
        :param comment: optional comment to invoice
        :param expire_in: timedelta object which indicates when invoice should be expired from now
        :param email: optional customer email
        :param timezone: timezone for invoice expiration
        :return: dict
        """
        url = '{}{}'.format(self.base_url, uuid.uuid4())
        timezone = pytz.timezone(timezone)
        expire_dt = timezone.localize(dt.datetime.now() + expire_in)

        payload = {
            'amount': {
                'currency': currency.upper(),
                'value': str(amount)
            },
            'expirationDateTime': expire_dt.isoformat(),
            'customer': {},

        }

        if comment:
            payload.update({
                'comment': comment
            })

        if email:
            payload['customer']['account'] = email

        self.api.make_request(url, method='put', headers=self.headers, data=json.dumps(payload))
        return Invoice.prepare(self.api.to_json())

    def check_bill(self, bill_id: str) -> Invoice:
        url = f'{self.base_url}{bill_id}'
        self.api.make_request(url, method='get', headers=self.headers)
        return Invoice.prepare(self.api.to_json())

    def cancel_bill(self, bill_id: str) -> Invoice:
        url = f'{self.base_url}{bill_id}/reject'
        headers = self.headers
        self.api.make_request(url, method='post', headers=headers)
        return Invoice.prepare(self.api.to_json())

    def refund_bill(self, amount: Decimal, bill_id: str, currency: str = 'RUB') -> Refund:
        url = f'{self.base_url}{bill_id}/refunds/{uuid.uuid4()}'
        payload = {
            'amount': {
                'currency': currency.upper(),
                'value': str(amount)
            }
        }
        self.api.make_request(url, method='put', data=json.dumps(payload), headers=self.headers)
        return Refund.prepare(self.api.to_json())

    def get_refund_status(self, refund_id: str):
        pass
