from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class PaymentStatus(StrEnum):
    WAITING = 'WAITING'
    PAID = 'PAID'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'


class RefundStatus(StrEnum):
    PARTIAL = 'PARTIAL'
    FULL = 'FULL'
