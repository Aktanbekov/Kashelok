# Generated by Django 4.1.5 on 2023-02-15 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PaysysHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.CharField(max_length=11, verbose_name="Количество денег"),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("uzs", "uzs"),
                            ("usd", "usd"),
                            ("eur", "eur"),
                            ("rub", "rub"),
                        ],
                        max_length=5,
                        verbose_name="Валюта",
                    ),
                ),
                (
                    "partner_trans_id",
                    models.UUIDField(verbose_name="ID partner_trans_id транзакции"),
                ),
                (
                    "client_ip_addr",
                    models.CharField(max_length=50, verbose_name="IP address"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                ("id_uuid", models.UUIDField(verbose_name="ID requests")),
                (
                    "result_transaction_id",
                    models.CharField(
                        default=0, max_length=100, verbose_name="ID transaction result"
                    ),
                ),
                (
                    "result_payment_id",
                    models.CharField(
                        default=0, max_length=100, verbose_name="ID payment result"
                    ),
                ),
                (
                    "response_id",
                    models.CharField(
                        default=0, max_length=100, verbose_name="ID response"
                    ),
                ),
                (
                    "response_mx_id",
                    models.CharField(
                        default=0, max_length=100, verbose_name="MX_ID response"
                    ),
                ),
                (
                    "error_response",
                    models.CharField(
                        blank=True,
                        default=0,
                        max_length=100,
                        verbose_name="error response",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_history",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]