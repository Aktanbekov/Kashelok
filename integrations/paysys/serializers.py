import requests, json

from rest_framework import serializers
from rest_framework import exceptions

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.payment.models import Payment, Transaction, PaymentChoices
from apps.users.models import User

from integrations.paysys.services import (get_client_ip, data_request, decode_token, get_headers_auth,
                                          data_check_payment_request, generate_uuid, data_cancel_payment_request)

from core.settings import PAYSYS_URL
from core.exceptions import MyException
from decimal import Decimal


class PaySysPaymentSerializer(serializers.ModelSerializer):
    card_holder_name = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True)
    card_expire = serializers.CharField(write_only=True)
    card_cvc = serializers.CharField(write_only=True)
    partner_trans_id = serializers.ReadOnlyField(source='transaction.partner_id')

    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'service_name', 'amount', 'currency',
            'status', 'client_ip_addr', 'description',
            'payment_id', 'transaction_id', 'mx_id', 'confirm_url', 'error', 'pay_id',
            'card_holder_name', 'card_number', 'card_expire', 'card_cvc',
            'partner_trans_id',
        )
        read_only_fields = (
            'user', 'status', 'client_ip_addr', 'mx_id', 'payment_id', 'confirm_url', 'error',
            'transaction_id', 'pay_id'
        )

    def create(self, validated_data):
        partner_trans_id = generate_uuid()
        response = requests.post(url=PAYSYS_URL, headers=get_headers_auth(),
                                 json=data_request(self, validated_data=validated_data,
                                                   partner_trans_id=partner_trans_id))

        response_dict: dict = response.json()

        if response_dict.get('error') != None:
            raise exceptions.ParseError(detail={'msg': 'Wrong input data'})

        paysys = Payment.objects.create(

            integration='paysys',

            user=decode_token(self).get('user_id'),

            service_name=validated_data.get('service_name'),

            amount=int(validated_data.get('amount')) / 100,

            currency=validated_data.get('currency'),

            description=validated_data.get('description'),

            client_ip_addr=get_client_ip(self.context.get('request')),

            pay_id=data_request(self, validated_data, partner_trans_id=partner_trans_id).get('id'),

            error=response_dict.get('error'),

            mx_id=response_dict.get('mx_id'),

            confirm_url=response_dict.get('result').get('confirm_url'),

            payment_id=response_dict.get('result').get('payment_id'),

            transaction_id=response_dict.get('result').get('transaction_id')

        )

        Transaction.objects.create(

            partner_id=partner_trans_id,

            payment_db=paysys

        )
        return paysys


class PaySysCancelPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'partner_id', 'payment_db')
        read_only_fields = ('payment_db',)

    def create(self, validated_data):
        transaction: Transaction = get_object_or_404(Transaction, partner_id=validated_data.get('partner_id'))
        response = requests.post(PAYSYS_URL, headers=get_headers_auth(),
                                 data=data_cancel_payment_request(validated_data))
        if response.status_code != 200:
            raise exceptions.ValidationError(detail={'msg': 'Wrong requests'})
        response_dict: dict = response.json()
        if response_dict['error'] != None:
            raise exceptions.ValidationError(detail={'msg': response_dict['error']}, code='400')
        transaction.payment_db.status = PaymentChoices.Cancelled
        transaction.payment_db.save()
        user = get_object_or_404(User, id=transaction.payment_db.user)
        user.balance -= Decimal(transaction.payment_db.amount)
        user.save()

        return transaction


class PaysysCheckPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'partner_id', 'add_balance')
        read_only_fields = ('add_balance',)

    @transaction.atomic
    def create(self, validated_data):
        transaction: Transaction = get_object_or_404(Transaction, partner_id=validated_data.get('partner_id'))
        response = requests.post(url=PAYSYS_URL, headers=get_headers_auth(),
                                 json=data_check_payment_request(validated_data=validated_data))
        response_dict: dict = response.json()
        if response.status_code != 200:
            raise exceptions.ValidationError(detail={'msg': 'Wrong requests'})
        if response_dict['error'] != None:
            raise exceptions.ValidationError(detail={'msg': response_dict['error']}, code='400')

        status = response_dict['result']['status']
        if status == '2' and not transaction.add_balance:
            user = get_object_or_404(User, id=transaction.payment_db.user)
            # exchange_rate: Decimal = get_exchange_rates(currency=paysys_history.currency)
            user.balance += Decimal(transaction.payment_db.amount)
            user.save()
            transaction.add_balance = True
            transaction.save()
            transaction.payment_db.status = PaymentChoices.Accepted
            transaction.payment_db.save()

        return transaction
