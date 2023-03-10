from rest_framework import serializers
from rest_framework import status
from rest_framework.serializers import ValidationError

from django.db import transaction

from apps.payments.models import Payment
from apps.payments.helpers import UrlKassa24
from apps.payments.models import PaymentStatus
from apps.payments.services import create_payment_object, response_check_status_kassa24, response_payment_to

import uuid
from decimal import Decimal


class SendMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("service_id", "requisite_db", "amount_db")

    @transaction.atomic
    def create(self, validated_data):
        local_id = uuid.uuid4()
        # достаем id комании
        service_id = validated_data.get("service_id")
        # достаем реквизиты 
        requisite = validated_data.get("requisite_db")
        # достаем количество денег для перевода !!!
        amount = int(Decimal(validated_data.get("amount_db")))
        # достаем запрос
        request = self.context["request"]

        # из запроса достаем баланс юзера и сравниваем с суммой перевода
        if request.user.balance <= amount:
            raise ValidationError(detail={"msg": "У вас не хватает денег для перевода"})
        
        # если средств достаточно создаем payment 
        payment = create_payment_object(
            # даем данные юзера, id_оплаты, статус в ожидании, доп инфо
            request.user, local_id, PaymentStatus.Pending, **validated_data
        )

        # создаем экземпляр кассы
        kassa24_url_obj = UrlKassa24()
        # проверяем статус оплаты 
        response = response_check_status_kassa24(
            kassa24_url_obj, local_id, requisite
        )
        # если статус failed то не совершаем оплату и кидаем ошибку
        if response.text.find('<ErrorMessage i:nil="true"/>') != -1:
            payment.status = PaymentStatus.Failed
            payment.save()
            raise ValidationError(detail={"msg": status.HTTP_400_BAD_REQUEST})

        # если статус проходит требования производится оплата
        response_pay = response_payment_to(
            kassa24_url_obj, local_id, service_id, requisite, amount
        )
        # проверяем стутус на неполадки сервера и прокидываем ошибку
        if response_pay.status_code != 200:
            payment.status = PaymentStatus.Failed
            payment.save()
            raise ValidationError(
                {
                    "msg": "Неполадки в сервере",
                    "status": status.HTTP_409_CONFLICT,
                }
            )
        # если статусы в норме и оплата прошла сохроняем положительный статус
        payment.status = PaymentStatus.Accepted
        # снимем с баланса сумму отправки
        payment.user.balance -= amount
        # сохроняем юзера
        payment.user.save()
        # сохроняем оплату
        payment.save()
        return payment

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["msg"] = "Платеж прошела успешно"
        return rep


class HistoryPaymentMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'id', 'service_id', 'amount_db', 'local_id', 'requisite_db', 'status', 'date',)


class HistoryPaymentAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'id', 'service_id', 'amount_db', 'local_id', 'requisite_db', 'status', 'date',)


class HistoryPaymentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'id', 'service_id', 'amount_db', 'local_id', 'requisite_db', 'status', 'date',)
