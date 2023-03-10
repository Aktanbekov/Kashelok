from django.urls import path
from integrations.paysys.views import PaySysPaymentView, PaysysCheckPaymentView, PaysysCancelView

urlpatterns = [
    path('payment/', PaySysPaymentView.as_view(), name='Pay to with Paysys'),
    path('cancel/', PaysysCancelView.as_view(), name='Cancel money from Paysys'),
    path('check/', PaysysCheckPaymentView.as_view(), name='Cancel money from Paysys'),
]
