from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import permissions

from django.db import transaction
from django.shortcuts import  get_object_or_404

from apps.paysys.models import PaysysHistory
from apps.paysys.serializers import (PaySysTranslationSerializer, PaySysCancelPaymentSerializer,
                                     PaysysCheckPaymentSerializer)
from apps.paysys.services import (get_headers_to_requests, get_uuid4,
                                  get_data_payment_to_requests, created_paysys_history,
                                  get_data_check_payment_to_requests, get_data_cancel_payment_to_requests,
                                  get_exchange_rates,)

from core.settings import PAYSYS_URL, PAYSYS_VENDOR_ID

import requests

from decimal import Decimal


class PaySysTranslationView(CreateAPIView):
    queryset = PaysysHistory.objects.all()
    serializer_class = PaySysTranslationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        id_uuid = get_uuid4()
        partner_trans_id_uuid = get_uuid4()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        headers: dict = get_headers_to_requests()
        data: dict = get_data_payment_to_requests(serializer_obj=serializer, PAYSYS_VENDOR_ID=PAYSYS_VENDOR_ID,
                                            partner_trans_id_uuid=partner_trans_id_uuid, id_uuid=id_uuid)

        response = requests.post(PAYSYS_URL, json=data, headers=headers)
        response_dict: dict = response.json()
        response_dict['partner_trans_id_uuid'] = partner_trans_id_uuid 

        if response.status_code != 200:
            raise exceptions.ValidationError({'msg': 'Problems in server'})

        if response_dict.get('error') != None:
            print(response.json())
            raise exceptions.ValidationError({'msg': 'You you entered incorrect data'})

        created_paysys_history(request=request, partner_trans_id_uuid=partner_trans_id_uuid,
                                                id_uuid=id_uuid,
                                                serializer_obj=serializer, response_dict=response_dict)

        return Response(response_dict)

            
class PaysysCancelView(CreateAPIView):
    queryset = PaysysHistory.objects.all()
    serializer_class = PaySysCancelPaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer: PaySysCancelPaymentSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_uuid: str =  get_uuid4()

        partner_trans_id = serializer.data.get('partner_trans_id')

        headers: dict = get_headers_to_requests()

        data: dict = get_data_cancel_payment_to_requests(partner_trans_id=partner_trans_id, id_uuid=id_uuid) 
        
        response = requests.post(PAYSYS_URL, json=data, headers=headers)
        response_dict: dict = response.json()
        return Response(response_dict)


class PaysysCheckPaymentView(CreateAPIView):
    queryset = PaysysHistory.objects.all()
    serializer_class = PaysysCheckPaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_uuid = get_uuid4()
        
        partner_trans_id: str = serializer.data.get('partner_trans_id')

        headers: dict = get_headers_to_requests()

        data: dict = get_data_check_payment_to_requests(partner_trans_id=partner_trans_id, id_uuid=id_uuid)
        response = requests.post(PAYSYS_URL, json=data, headers=headers)

        response_dict: dict = response.json()
        status = response_dict['result']['status']
        paysys_history = get_object_or_404(PaysysHistory, partner_trans_id=partner_trans_id)
        if status == '2' and not paysys_history.add_balance:
            exchange_rate: Decimal = get_exchange_rates(currency=paysys_history.currency)
            paysys_history.user.balance += (Decimal(paysys_history.amount) * exchange_rate)
            paysys_history.user.save()
            paysys_history.add_balance = True
            paysys_history.save()
            
        return Response(response_dict)
            
