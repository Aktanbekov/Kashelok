from django.db import models
from apps.users.models import User

from apps.users.models import User


class PaysysHistory(models.Model):
    current_choice = (
        ('uzs', 'uzs'), ('usd', 'usd'), ('eur', 'eur'), ('rub', 'rub'),
    )

    amount = models.CharField(verbose_name='Количество денег', max_length=11)
    currency = models.CharField(verbose_name='Валюта', choices=current_choice, max_length=5)
    partner_trans_id = models.UUIDField(verbose_name='ID partner_trans_id транзакции')
    client_ip_addr = models.CharField(verbose_name='IP address', max_length=50)
    description = models.TextField(verbose_name='description', blank=True, null=True)
    id_uuid = models.UUIDField(verbose_name='ID requests')
    result_transaction_id = models.CharField(verbose_name='ID transaction result', max_length=100, default=0)
    result_payment_id = models.CharField(verbose_name='ID payment result', max_length=100, default=0)
    response_id = models.CharField(verbose_name='ID response', max_length=100, default=0)
    response_mx_id = models.CharField(verbose_name='MX_ID response', max_length=100, default=0)
    error_response = models.CharField(verbose_name='error response', max_length=100, blank=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_history')
    add_balance = models.BooleanField(verbose_name='Check add balance', default=False)

    def __str__(self) -> str:
        return f'{self.amount} som'
    