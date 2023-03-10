from django.contrib import admin
from apps.kassa_services.models import Service, KassaService



class ServiceInline(admin.TabularInline):
    model = Service


class PaymentServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceInline, ]


admin.site.register(KassaService, PaymentServiceAdmin)
admin.site.register(Service)