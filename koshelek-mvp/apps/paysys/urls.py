from django.urls import path
from apps.paysys.views import PaySysTranslationView, PaysysCancelView, PaysysCheckPaymentView

urlpatterns = [
    path('paysys_to/', PaySysTranslationView.as_view(), name='Pay to with Paysys'),
    path('paysys_cancel/', PaysysCancelView.as_view(), name='Cancel money from Paysys'),
    path('paysys_check_payment/', PaysysCheckPaymentView.as_view(), name='Check payment'),
    
]
