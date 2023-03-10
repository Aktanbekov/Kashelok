from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.users.managers import CustomUserManager
from apps.users.tasks import send_otp_to_phone


class User(AbstractUser):
    phone_number = models.CharField(verbose_name='phone number', unique=True, max_length=15)
    balance = models.DecimalField(verbose_name='balance', max_digits=99, decimal_places=2, default=0)
    email = models.EmailField(verbose_name='email address', null=True, blank=True) #uniqie =True
    username = models.CharField(verbose_name="username", max_length=31, null=True, blank=True)
    first_name = models.CharField(verbose_name="first name", max_length=31, blank=True, null=True)
    last_name = models.CharField(verbose_name="last name", max_length=31, blank=True, null=True)
    surname = models.CharField(verbose_name="surname", max_length=31, blank=True, null=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number}'


@receiver(post_save, sender=User)
def send_verification_code(sender, instance, created, **kwargs):
    if created:
        message = f"Activation code {instance.code}"
        send_otp_to_phone(phone_number=instance.phone_number, message=message)  # local
        # send_otp_to_phone.delay(phone_number=instance.phone_number, message=message) #prod
