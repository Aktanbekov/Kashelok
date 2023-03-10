from django.db import models
from apps.kassa_services.models import Service


class PaymentChoices:
    current_choice = (
        ('uzs', 'uzs'), ('usd', 'usd'), ('eur', 'eur'), ('rub', 'rub'),
    )

    payment_integration_choices = (
        ('kassa24', 'kassa24'), ('paysys', 'paysys'),
    )

    Accepted = 2  # Принят
    Pending = 3  # В ожидании
    Processing = 4  # Обрабатывается
    Completed = 5  # Проведен
    Failed = 6  # Неудача
    Cancelled = 7  # Отменен
    ForciblyCanceled = 8  # Принудительно отменен
    CancelFailed = 9  # Неудача при отмене
    PartlyCanceled = 10  # Частичная отмена

    status = (
        (Accepted, "Принят"),
        (Pending, "В ожидании"),
        (Processing, "Обрабатывается"),
        (Completed, "Проведен"),
        (Failed, "Неудача"),
        (Cancelled, "Отменен"),
        (ForciblyCanceled, "Принудительно отменен"),
        (CancelFailed, "Неудача при отмене"),
        (PartlyCanceled, "Частичная отмена"),
    )


class Payment(models.Model):
    # kassa24
    service_id = models.ForeignKey(to=Service, on_delete=models.DO_NOTHING, related_name='payment', null=True,
                                   blank=True)
    requisite = models.CharField(verbose_name="Реквизиты", max_length=200, blank=True, null=True)

    amount = models.CharField(verbose_name='Количество денег', max_length=11)
    user = models.IntegerField(verbose_name='User ID')
    status = models.CharField(max_length=100, choices=PaymentChoices.status, default=PaymentChoices.Pending)

    # owner
    created_at = models.DateTimeField(verbose_name='DateTime requests ', auto_now_add=True)
    integration = models.CharField(verbose_name='Integration use',
                                   choices=PaymentChoices.payment_integration_choices,
                                   max_length=50, null=False)

    # Paysys
    service_name = models.CharField(verbose_name='Service name', max_length=100, null=True, blank=True)
    currency = models.CharField(verbose_name='Валюта', choices=PaymentChoices.current_choice, max_length=5, null=True,
                                blank=True)
    client_ip_addr = models.CharField(verbose_name='IP address', max_length=50, null=True, blank=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)

    # response 
    payment_id = models.IntegerField(verbose_name='payment id transaction', null=True)  # Integer fields
    transaction_id = models.CharField(verbose_name='ID transaction result', max_length=100)
    mx_id = models.CharField(verbose_name='MX_ID response', max_length=100, null=True)
    confirm_url = models.CharField(verbose_name='confirm url', max_length=100, null=True, blank=True)
    error = models.CharField(verbose_name='error response', max_length=100, null=True, blank=True)
    pay_id = models.CharField(verbose_name='pay id', max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.id}) Payment <{self.integration}, {self.created_at}>'


class Transaction(models.Model):
    partner_id = models.UUIDField(verbose_name='partner_trans_id or local_id')
    payment_db = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='transaction')
    add_balance = models.BooleanField(verbose_name='add balance', default=False)

    def __str__(self):
        return f'{self.id}) Transaction -> Date={self.payment_db.created_at.ctime()} -> error={self.payment_db.error}>'
