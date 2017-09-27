from django.db import models


class BTCSellOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='SELLBTC')


class BTCBuyOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='BUYBTC')
