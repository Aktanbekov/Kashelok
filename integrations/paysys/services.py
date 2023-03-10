import calendar
import time
import hashlib
import uuid
import jwt
from rest_framework import exceptions

from core.settings import PAYSYS_SECRET_KEY, PAYSYS_SERVICE_ID, PAYSYS_VENDOR_ID, SECRET_KEY, PAYSYS_URL


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_headers_auth():
    current_GMT = time.gmtime()
    time_stamp = str(calendar.timegm(current_GMT))
    payload = f'{PAYSYS_SECRET_KEY}{time_stamp}'
    hash_object = hashlib.sha1(payload.encode())
    pbHash = hash_object.hexdigest()
    hash_id = f'{PAYSYS_SERVICE_ID}-{pbHash}-{time_stamp}'
    headers = {'Auth': hash_id}

    return headers


def data_request(self, validated_data, partner_trans_id):
    data = {
        "method": "paysys.prepare_payment",
        "params": {
            "card_holder_name": validated_data.get('card_holder_name'),
            "card_number": validated_data.get('card_number'),
            "card_expire": validated_data.get('card_expire'),
            "card_cvc": validated_data.get('card_cvc'),
            "amount": validated_data.get('amount'),
            "currency": validated_data.get('currency'),
            "vendor_id": PAYSYS_VENDOR_ID,
            "partner_trans_id": partner_trans_id,
            "client_ip_addr": "143.42.17.183",
            "description": validated_data.get('description'),
            "redirect_url": "https://143.42.17.183"
        },
        "id": generate_uuid()
    }

    return data


def decode_token(self):
    user_token: str = self.context.get('request').headers.get('Authorization', None)
    if user_token is None:
        raise exceptions.NotAuthenticated(detail={'msg': "You do not Authenticated", }, code='403')
    valid_token = user_token.split(' ')[-1]
    secret = SECRET_KEY
    jwt_options = {
        'verify_signature': False,
        'verify_exp': True,
    }
    decoded = jwt.decode(valid_token, secret, algorithms=['HS256'], options=jwt_options)
    return decoded


def data_check_payment_request(validated_data: dict):
    data = {
        "method": "paysys.check_payment",
        "params": {
            "partner_trans_id": str(validated_data.get('partner_id'))
        },
        "id": generate_uuid()
    }
    return data


def data_cancel_payment_request(partner_trans_id: str):
    data = {
        "method": "paysys.cancel_payment",
        "params": {
            "partner_trans_id": str(partner_trans_id)
        },
        "id": generate_uuid()
    }
    return data
