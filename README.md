# Python Qiwi API client

## Description
Python client for Qiwi Payments API (Qiwi Kassa, Qiwi Wallet)

## Install
```bash
pip install qiwi-payments
```

## Usage
```python
from decimal import Decimal

from qiwi_payments.kassa import QiwiKassa

kassa = QiwiKassa('MY_SECRET_QIWI_KEY')
invoice = kassa.create_bill(
    amount=Decimal('10.00'),
    currency='RUB',
    comment='Pay me ASAP'
)

print(invoice.pay_url)
```
