from django.urls import path
from .views import PayToView, HistoryPaymentMeView, HistoryPaymentAllView, HistoryPaymentRetrieveView

urlpatterns = [
    path("pay_to/", PayToView.as_view(), name="Pay_to"),
    path('history_me/', HistoryPaymentMeView.as_view(), name='History_me'),
    path('history_all/', HistoryPaymentAllView.as_view(), name='History_all'),
    path('history_retrieve/<int:pk>', HistoryPaymentRetrieveView.as_view(), name='History_retrieve')
]
