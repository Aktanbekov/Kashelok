from rest_framework.generics import ListAPIView
from apps.kassa_services.models import Service, KassaService
from apps.kassa_services.serializers import ServiceListSerializer, KassaServiceSerializer


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer


class KassaServicesListView(ListAPIView):
    queryset = KassaService.objects.all()
    serializer_class = KassaServiceSerializer
