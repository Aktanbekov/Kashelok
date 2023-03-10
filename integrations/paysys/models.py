from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import exceptions

from apps.payment.models import Transaction, PaymentChoices
from apps.users.models import User
from integrations.paysys.services import get_headers_auth, data_cancel_payment_request
from core.settings import PAYSYS_URL

from decimal import Decimal

import requests


class PaysysCancel(models.Model):
    transaction = models.ForeignKey(to=Transaction, on_delete=models.CASCADE, related_name='cancel',
                                    help_text='Выберите транзакцию по которой произойдет отмена платежа')
    error = models.CharField(verbose_name='cancel error', max_length=100, null=True, blank=True,
                             help_text="Не заполняйте это поле ^")
    done = models.BooleanField(default=False)

    def save(self) -> None:
        if self.done and self.transaction.payment_db.status == PaymentChoices.Accepted:
            # transaction: Transaction = get_object_or_404(Transaction, partner_id=self.transaction.partner_id)
            response = requests.post(PAYSYS_URL, headers=get_headers_auth(),
                                     json=data_cancel_payment_request(self.transaction.partner_id))
            print(response.json())
            if response.status_code != 200:
                self.done = False
                self.error = "Проблемы с Paysys"
                return super().save()
                # raise exceptions.ValidationError(detail={'msg': 'Wrong requests'})
            response_dict: dict = response.json()
            if response_dict['error'] != None:
                self.done = False
                self.error = response_dict.get('error').get('message')
                return super().save()
                # raise exceptions.ValidationError(detail={'msg': response_dict['error']})
            self.transaction.payment_db.status = PaymentChoices.Cancelled
            self.transaction.payment_db.save()
            user = get_object_or_404(User, id=self.transaction.payment_db.user)
            user.balance += Decimal(self.transaction.payment_db.amount)
            user.save()
        else:
            self.done = False
            self.error = 'Вы не поставили галочку на поле done или выбрали не правильный transaction'
        return super().save()

    def __str__(self):
        return f'Cancel status=({self.done}) -> date={self.transaction.payment_db.created_at.ctime()} -> error={self.error}'
