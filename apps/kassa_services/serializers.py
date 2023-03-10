from rest_framework import serializers

from apps.kassa_services.models import Service, KassaService


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name',
                  'operator_service', 'min_amount', 'max_amount', 'commission', 'prefix')


class KassaServiceSerializer(serializers.ModelSerializer):
    services = ServiceListSerializer(read_only=True, many=True)

    class Meta:
        model = KassaService
        fields = ('id', 'name', 'services',)
