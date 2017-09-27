from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import BTCBuyOrderManager, BTCSellOrderManager

ORDER_STATES = (
    ('PENDING', 'Pending order'),
    ('EXECUTED', 'Executed order'),
    ('CANCELLED', 'Cancelled order')
)

ORDER_TYPE = (
    ('BUYBTC', 'BTC Buy Order'),
    ('SELLBTC', 'BTC Sell Order')
)


class User(AbstractUser):
    date_of_birth = models.DateField('date of birth', null=True)
    tax_id = models.CharField('tax id', max_length=32, null=True)

    class Meta:
        ordering = '-date_joined',

    def __str__(self):
        return self.username


class BillingAccount(models.Model):
    user = models.ForeignKey('User', related_name='billing_account')
    balance_brl = models.DecimalField('BRL balance', max_digits=15, decimal_places=6)
    balance_btc = models.DecimalField('BTC balance', max_digits=15, decimal_places=6)
    active = models.BooleanField('active', default=True)

    # Audit fields
    created_at = models.DateTimeField('created at', auto_now_add=True)
    modified_at = models.DateTimeField('modified at', auto_now=True)

    class Meta:
        ordering = '-created_at',

    def __str__(self):
        return '{} - BRL {} - BTC {}'.format(self.user.username, self.balance_brl, self.balance_btc)


class BTCOrder(models.Model):
    type = models.CharField('type', max_length=255, choices=ORDER_TYPE)
    billing_account = models.ForeignKey('BillingAccount', related_name='sell_orders')
    order_state = models.CharField('state', max_length=255, choices=ORDER_STATES)
    amount_brl = models.DecimalField('BRL amount', max_digits=15, decimal_places=6)
    amount_btc = models.DecimalField('BTC amount', max_digits=15, decimal_places=6)

    # Audit fields
    created_at = models.DateTimeField('created at', auto_now_add=True)
    modified_at = models.DateTimeField('modified at', auto_now=True)

    class Meta:
        ordering = '-created_at',
        verbose_name = 'BTC Order'
        verbose_name_plural = 'BTC Orders'

    @property
    def exchange_rate(self):
        return self.amount_brl / self.amount_btc

    def __str__(self):
        return '{} - {} - BTC {} - BRL {} - {} BRL/BTC'.format(
            self.billing_account.user.username,
            self.order_state,
            self.amount_btc,
            self.amount_brl,
            self.exchange_rate
        )


class BTCSellOrder(BTCOrder):
    objects = BTCSellOrderManager()

    class Meta:
        proxy = True
        verbose_name = 'BTC Sell Order'
        verbose_name_plural = 'BTC Sell Orders'


class BTCBuyOrder(BTCOrder):
    objects = BTCBuyOrderManager()

    class Meta:
        proxy = True
        verbose_name = 'BTC Buy Order'
        verbose_name_plural = 'BTC Buy Orders'
