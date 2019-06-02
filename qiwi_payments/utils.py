import hmac
import base64
import hashlib
import logging
from typing import Union, Optional

from requests import (
    request as do_request,
    Timeout,
    HTTPError,
    RequestException,
    Response,
)

from qiwi_payments.models import Invoice

logger = logging.getLogger(__name__)


class APIError(Exception):
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        self.request = kwargs.pop('request', None)


class HttpClient(object):
    def __init__(self):
        self.response = None

    def make_request(self,
                     url: str,
                     params: Optional[dict] = None,
                     headers: Optional[dict] = None,
                     timeout: tuple = (15, 60),
                     method: str = 'get',
                     data: Union[dict, str, None] = None,
                     response_encoding: Optional[str] = None,
                     **kwargs) -> Response:

        try:
            logger.debug(f'Making request to {url}')
            response = do_request(method, url,
                                  timeout=timeout, params=params,
                                  headers=headers, data=data, **kwargs)
            response.raise_for_status()
        except HTTPError as e:
            response = e.response
            logger.error(
                f'HTTPError with HTTP status: {response.status_code} @ {url}. '
                f'Response: {response.content}'
            )
            logger.exception(e)
            raise APIError(f'HTTP Error occured. Status {response.status_code}',
                           response=response) from e
        except Timeout as e:
            logger.error(
                f'Connection timeout: {url}. Timeout settings {timeout}'
            )
            logger.exception(e)
            raise APIError(f'Time is out. Value: {timeout}') from e
        except RequestException as e:
            logger.exception(e)
            raise APIError(f'Request Exception occured') from e
        else:
            self.response = response

        if response_encoding:
            self.response.encoding = response_encoding

        return self.response

    def to_json(self):
        try:
            result = self.response.json()
        except ValueError as e:
            raise APIError(f'Invalid JSON body: {self.response.content}') from e
        else:
            return result


def generate_hmac_hash(invoice: Invoice, secret_key: str) -> bytes:
    invoice_params = [
        f'{invoice.amount.currency}',
        f'{invoice.amount.value}',
        f'{invoice.bill_id}',
        f'{invoice.site_id}',
        f'{invoice.status.value}',
    ]
    string = '|'.join(invoice_params)
    digest = hmac.HMAC(
        secret_key.encode('utf-8'),
        string.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    return digest.hexdigest()
