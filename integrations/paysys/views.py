from rest_framework.generics import CreateAPIView

from rest_framework import permissions

from integrations.paysys.serializers import PaySysPaymentSerializer, PaySysCancelPaymentSerializer, \
    PaysysCheckPaymentSerializer
from apps.payment.models import Payment, Transaction


class PaySysPaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaySysPaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PaysysCancelView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaySysCancelPaymentSerializer


class PaysysCheckPaymentView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = PaysysCheckPaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)
