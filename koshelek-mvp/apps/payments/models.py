from django.db import models
from apps.users.models import User

from core.settings import KASSA_LOGIN, KASSA_PASSWORD


class PaymentStatus:
    Accepted = 2          # Принят
    Pending = 3           # В ожидании
    Processing = 4        # Обрабатывается
    Completed = 5         # Проведен
    Failed = 6            # Неудача
    Cancelled = 7         # Отменен
    ForciblyCanceled = 8  # Принудительно отменен
    CancelFailed = 9      # Неудача при отмене
    PartlyCanceled = 10   # Частичная отмена

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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="payment")
    service_id = models.CharField(verbose_name="ID компании", max_length=200)
    amount_db = models.IntegerField(verbose_name="Количество денег",)
    local_id = models.UUIDField(verbose_name="локальный айдишник")
    requisite_db = models.CharField(verbose_name="Реквизиты", max_length=200)
    status = models.CharField(verbose_name="Статусы", choices=PaymentStatus.status, max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}-payment_pk, {self.user}'

    login = KASSA_LOGIN
    password = KASSA_PASSWORD
    serviceId = ""        # id компании который нам дают 3043
    amount = ""           # количества денег
    localId = ""          # наш id
    requisite = ""        # номер телефона который у нас в базе
    receiptId = ""        # номер чека
    paymentID = ""        # Ваш id
    dateFrom = ""
    dateTo = ""
    reportID = ""
    IP_address = "https://kassa24.kg"  # kassa24
