# Generated by Django 4.1.5 on 2023-02-02 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="amount_db",
            field=models.IntegerField(verbose_name="Количество денег"),
        ),
    ]