from rest_framework import serializers

from apps.paysys.models import PaysysHistory


class PaySysTranslationSerializer(serializers.ModelSerializer):
    card_holder_name = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True)
    card_expire = serializers.CharField(write_only=True)
    card_cvc = serializers.CharField(write_only=True)

    class Meta:
        model = PaysysHistory
        fields = ('amount', 'currency', 'client_ip_addr', 'description',
                  'card_holder_name', 'card_number', 'card_expire', 'card_cvc')


class PaySysCancelPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaysysHistory
        fields = ('id', 'partner_trans_id')


class PaysysCheckPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaysysHistory
        fields = ('id', 'partner_trans_id',)