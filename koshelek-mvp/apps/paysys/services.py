from apps.paysys.models import PaysysHistory

from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions

from core.settings import PAYSYS_SERVICE_ID, PAYSYS_SECRET_KEY

from decimal import Decimal

import uuid
import time
import hashlib


def get_headers_to_requests():
    time_in_second = round(time.time() * 1000)

    hash_encode = hashlib.sha1(f'{PAYSYS_SECRET_KEY}{time_in_second}'.encode())

    hash_ = hash_encode.hexdigest()

    headers = {
        'Auth': f'{PAYSYS_SERVICE_ID}-{hash_}-{time_in_second}',
        'Content-Type': 'application/json'
    }
    return headers


def get_uuid4():
    return str(uuid.uuid4())


def get_data_payment_to_requests(serializer_obj: ModelSerializer, PAYSYS_VENDOR_ID,
                                 partner_trans_id_uuid, id_uuid):
    card_holder_name = serializer_obj.validated_data.get('card_holder_name')
    card_number = serializer_obj.validated_data.get('card_number')
    card_expire = serializer_obj.validated_data.get('card_expire')
    card_cvc = serializer_obj.validated_data.get('card_cvc')
    amount = serializer_obj.data['amount']
    currency = serializer_obj.data['currency']
    client_ip_addr = serializer_obj.data['client_ip_addr']
    description = serializer_obj.data['description']

    data = {
        "method": "paysys.prepare_payment",
        "params": {
            "card_holder_name": card_holder_name,
            "card_number": card_number,
            "card_expire": card_expire,
            "card_cvc": card_cvc,
            "amount": amount,
            "currency": currency,
            "vendor_id": PAYSYS_VENDOR_ID,
            "partner_trans_id": partner_trans_id_uuid,
            "client_ip_addr": client_ip_addr,
            "description": description,
            "redirect_url": "http://sportsupport.store"
        },
        "id": id_uuid
    }
    return data


def created_paysys_history(request, partner_trans_id_uuid, id_uuid, serializer_obj, response_dict):
    serializer_data_copy = serializer_obj.data.copy()
    amount = Decimal(serializer_data_copy.pop('amount')) / 100
    paysys_history: PaysysHistory = PaysysHistory.objects.create(partner_trans_id=partner_trans_id_uuid,
                                                                 id_uuid=id_uuid,
                                                                 user=request.user,
                                                                 amount=amount,
                                                                 **serializer_data_copy)
    
    paysys_history.result_transaction_id = response_dict["result"]["transaction_id"]
    paysys_history.result_payment_id = response_dict["result"]["payment_id"]
    paysys_history.result_response_id = response_dict["id"]
    paysys_history.result_response_mx_id = response_dict["mx_id"]
    paysys_history.error_response = 'Nonee' if response_dict['error'] == None else ''
    paysys_history.save()
    return paysys_history


def get_data_check_payment_to_requests(partner_trans_id, id_uuid):
    data = {
        "method": "paysys.check_payment",
        "params": {
            "partner_trans_id": partner_trans_id
        },
        "id": id_uuid
    }
    return data


def get_data_cancel_payment_to_requests(partner_trans_id, id_uuid):
    data = {
                "method": "paysys.cancel_payment",
                "params": {
                    "partner_trans_id": partner_trans_id
                },
                "id": id_uuid
            }
    return data

def get_exchange_rates(currency):
    rub = Decimal(1.2090)
    usd = Decimal(88.30)
    eur = Decimal(94.74)
    uzs = Decimal(0.0077)
    if currency == 'rub':
        return rub
    elif currency == 'usd':
        return usd
    elif currency == 'eur':
        return eur
    elif currency == 'uzs':
        return uzs
    else:
        raise exceptions.ValidationError({'msg': 'Wrong currency'})
