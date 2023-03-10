from rest_framework import serializers
from rest_framework import status
from rest_framework.serializers import ValidationError

from django.db import transaction

from apps.payment.models import Payment, PaymentChoices, Service

from integrations.kassa24.helpers import UrlKassa24
from integrations.kassa24.services import generate_uuid, create_payment_object, response_check_status_kassa24, \
    response_payment_to

from decimal import Decimal


class PayToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("service_id", "requisite", "amount")

    @transaction.atomic
    def create(self, validated_data):
        local_id = generate_uuid()
        service: Service = validated_data.get("service_id")
        requisite = validated_data.get("requisite")
        amount = int(Decimal(validated_data.get("amount")))
        request = self.context["request"]
        kassa24_url_obj = UrlKassa24()

        if request.user.balance <= amount:
            raise ValidationError(detail={"msg": "У вас не хватает денег для перевода"})

        response = response_check_status_kassa24(
            kassa24_url_obj, local_id, requisite
        )

        if response.text.find('<ErrorMessage i:nil="true"/>') != -1:
            raise ValidationError(detail={"msg": status.HTTP_400_BAD_REQUEST})

        response_pay = response_payment_to(
            kassa24_url_obj, local_id, service.service_id, requisite, amount
        )
        if response_pay.status_code != 200:
            raise ValidationError(
                {
                    "msg": "Неполадки в сервере",
                    "status": status.HTTP_409_CONFLICT,
                }
            )
        payment: Payment = create_payment_object(
            request.user, local_id, PaymentChoices.Accepted, **validated_data
        )

        request.user.balance -= amount
        request.user.save()
        return payment

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["msg"] = "Платеж прошела успешно"
        return rep


class HistoryPaymentSerializer(serializers.ModelSerializer):
    partner_id = serializers.ReadOnlyField(source='transaction.partner_id')

    class Meta:
        model = Payment
        fields = ('user', 'id', 'service_id', 'amount', 'requisite', 'status', 'created_at', 'partner_id')  # 'date',
