from django.urls import path

from apps.kassa_services.views import ServiceListView, KassaServicesListView

urlpatterns = [
    path('all/', ServiceListView.as_view(), name="Get all service"),
    path('name/', KassaServicesListView.as_view(), name='get name kassa service')
]
