from django.contrib import admin
from apps.payment.models import Payment, Transaction

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('partner_id', 'payment_db__created_at',)
    


admin.site.register(Payment)
admin.site.register(Transaction, TransactionAdmin)
