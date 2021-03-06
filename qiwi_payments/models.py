import datetime as dt
from decimal import Decimal
from typing import NamedTuple

from dateutil.parser import parse

from qiwi_payments.constants import PaymentStatus


class Amount(NamedTuple):
    currency: str
    value: Decimal

    def __repr__(self):
        return f'<Amount: {self.currency}{self.value}>'

    @classmethod
    def prepare(cls, data: dict) -> 'Amount':
        return cls(
            currency=data['amount']['currency'],
            value=Decimal(data['amount']['value'])
        )


class Status(NamedTuple):
    value: PaymentStatus
    datetime: dt.datetime

    def __repr__(self):
        return '<Status {}>'.format(self.value)

    @classmethod
    def prepare(cls, data: dict) -> 'Status':
        params = {
            'value': data['status']['value']
        }
        if 'datetime' in data['status']:
            params.update({
                'datetime': parse(data['status']['datetime'])
            })
        if 'changedDateTime' in data['status']:
            params.update({
                'datetime': parse(data['status']['changedDateTime'])
            })
        return cls(**params)


class Invoice(NamedTuple):
    site_id: str
    bill_id: str
    amount: Amount
    status: Status
    comment: str
    pay_url: str
    creation_dt: dt.date
    expiration_dt: dt.date
    customer: dict
    custom_fields: dict

    def __repr__(self):
        return '<Invoice {}>'.format(self.bill_id)

    @classmethod
    def prepare(cls, data: dict) -> 'Invoice':
        return cls(
            site_id=data['siteId'],
            bill_id=data['billId'],
            amount=Amount.prepare(data),
            status=Status.prepare(data),
            comment=data.get('comment', ''),
            creation_dt=parse(data['creationDateTime']),
            expiration_dt=parse(data['expirationDateTime']),
            pay_url=data.get('payUrl'),
            customer=data.get('customer', {}),
            custom_fields=data.get('customFields', {})
        )

    @property
    def is_paid(self):
        return self.status.value == PaymentStatus.PAID

    @property
    def is_canceled(self):
        return self.status.value == PaymentStatus.REJECTED

    @property
    def is_expired(self):
        return self.status.value == PaymentStatus.EXPIRED


class Refund(NamedTuple):
    amount: Amount
    dt: dt.datetime
    refund_id: str
    status: PaymentStatus

    def __repr__(self):
        return f'<Refund {self.refund_id}>'

    @classmethod
    def prepare(cls, data: dict) -> 'Refund':
        return cls(
            amount=Amount.prepare(data),
            dt=parse(data['datetime']),
            refund_id=data['refundId'],
            status=Status.prepare(data)
        )
