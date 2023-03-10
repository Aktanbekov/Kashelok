# Generated by Django 4.1.5 on 2023-03-09 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KassaService",
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
                    "image",
                    models.FileField(
                        upload_to="media/kassa24/service_name", verbose_name="photo"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="service name")),
            ],
        ),
        migrations.CreateModel(
            name="Service",
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
                    "service_id",
                    models.CharField(max_length=30, verbose_name="service id"),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "operator_service",
                    models.CharField(max_length=100, verbose_name="operator service"),
                ),
                ("min_amount", models.IntegerField(verbose_name="min amount")),
                ("max_amount", models.IntegerField(verbose_name="max amount")),
                ("commission", models.IntegerField(verbose_name="commission")),
                (
                    "prefix",
                    models.CharField(max_length=100, null=True, verbose_name="prefix"),
                ),
                (
                    "image",
                    models.FileField(
                        upload_to="media/kassa24/service", verbose_name="photo"
                    ),
                ),
                (
                    "kassa24_service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="kassa_services.kassaservice",
                    ),
                ),
            ],
        ),
    ]