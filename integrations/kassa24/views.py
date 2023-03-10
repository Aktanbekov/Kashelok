from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import permissions
from apps.payment.models import Payment
from integrations.kassa24.serializers import (
    PayToSerializer, HistoryPaymentSerializer, )
from integrations.kassa24.mixins import HistoryPaymentMeMixin
from integrations.kassa24.permission import OwnerPermission


class PayToView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PayToSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HistoryPaymentMeView(HistoryPaymentMeMixin, ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = HistoryPaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HistoryPaymentAllView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = HistoryPaymentSerializer
    permission_classes = (permissions.IsAdminUser,)


class HistoryPaymentRetrieveView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = HistoryPaymentSerializer
    permission_classes = (OwnerPermission,)
