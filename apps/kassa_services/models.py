from django.db import models


class KassaService(models.Model):
    image = models.FileField(verbose_name='photo', upload_to='media/kassa24/service_name')
    name = models.CharField(verbose_name='service name', max_length=100)

    def __str__(self):
        return f'PaymentService<{self.name}>'


class Service(models.Model):
    kassa24_service = models.ForeignKey(to=KassaService, on_delete=models.CASCADE, related_name="services")
    service_id = models.CharField(verbose_name='service id', max_length=30)
    name = models.CharField(verbose_name='name', max_length=100)
    operator_service = models.CharField(verbose_name='operator service', max_length=100)
    min_amount = models.IntegerField(verbose_name='min amount')
    max_amount = models.IntegerField(verbose_name='max amount')
    commission = models.IntegerField(verbose_name='commission')
    prefix = models.CharField(verbose_name='prefix', max_length=100, null=True)
    image = models.FileField(verbose_name='photo', upload_to='media/kassa24/service')

    def __repr__(self):
        return f'{self.id}'

    def __str__(self):
        return f'Service<{self.service_id} -> {self.name}>'
