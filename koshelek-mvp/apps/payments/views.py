from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import permissions

from apps.payments.models import Payment
from apps.payments.serializers import (
    SendMoneySerializer, HistoryPaymentMeSerializer, HistoryPaymentAllSerializer, HistoryPaymentRetrieveSerializer)
from apps.payments.mixins import HistoryPaymentMeMixin
from apps.payments.permission import OwnerPermission


class PayToView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = SendMoneySerializer
    permission_classes = (permissions.IsAuthenticated,)


class HistoryPaymentMeView(HistoryPaymentMeMixin, ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = HistoryPaymentMeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HistoryPaymentAllView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = HistoryPaymentAllSerializer
    permission_classes = (permissions.IsAdminUser,)


class HistoryPaymentRetrieveView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = HistoryPaymentRetrieveSerializer
    permission_classes = (OwnerPermission,)
