from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

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


class CryptAmount(models.DecimalField):
    description = 'CryptTrader amount'

    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [MinValueValidator(Decimal('0.01'))]
        kwargs['max_digits'] = 15
        kwargs['decimal_places'] = 6

        super().__init__(*args, **kwargs)


class User(AbstractUser):
    """
    Customized User model for CryptTrader.
    """
    date_of_birth = models.DateField('date of birth', null=True)
    tax_id = models.CharField('tax id', max_length=32, null=True)

    class Meta:
        ordering = '-date_joined',

    def __str__(self):
        return self.username


class BillingAccount(models.Model):
    """
    Billing account associated to a user.

    This class summarizes the data related to the billing account.
    """
    user = models.OneToOneField('User', related_name='billing_account')
    active = models.BooleanField('active', default=True)

    # Audit fields
    created_at = models.DateTimeField('created at', auto_now_add=True)
    modified_at = models.DateTimeField('modified at', auto_now=True)

    class Meta:
        ordering = '-created_at',

    @property
    def balance_btc(self):
        agg_func = Coalesce(Sum('amount_btc'), 0)
        buy_btc = self.orders.filter(type='BUYBTC', order_state='EXECUTED').aggregate(s=agg_func)['s']
        sell_btc = self.orders.filter(type='SELLBTC', order_state='EXECUTED').aggregate(s=agg_func)['s']
        return buy_btc - sell_btc

    @property
    def balance_brl(self):
        orders_states = ['EXECUTED', 'PENDING']
        agg_func = Coalesce(Sum('amount_brl'), 0)

        buy_brl = self.orders.filter(type='BUYBTC', order_state__in=orders_states).aggregate(s=agg_func)['s']
        sell_brl = self.orders.filter(type='SELLBTC', order_state='EXECUTED').aggregate(s=agg_func)['s']
        transferred = self.funds_transfers.filter(funds_transfer_state='EXECUTED').aggregate(s=agg_func)['s']
        return transferred + sell_brl - buy_brl

    def __str__(self):
        return '{} - BRL {} - BTC {}'.format(self.user.username, self.balance_brl, self.balance_btc)


class BTCOrder(models.Model):
    """
    Generic model that represents an order. It can be BUY or SELL BTCs.
    """
    type = models.CharField('type', max_length=255, choices=ORDER_TYPE, default='BUYBTC')
    billing_account = models.ForeignKey('BillingAccount', related_name='orders')
    order_state = models.CharField('state', max_length=255, choices=ORDER_STATES, default='PENDING')
    amount_brl = CryptAmount('BRL amount')
    amount_btc = CryptAmount('BTC amount')

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
    """Order to sell BTC."""
    objects = BTCSellOrderManager()

    class Meta:
        proxy = True
        verbose_name = 'BTC Sell Order'
        verbose_name_plural = 'BTC Sell Orders'


class BTCBuyOrder(BTCOrder):
    """Order to buy BTC."""
    objects = BTCBuyOrderManager()

    class Meta:
        proxy = True
        verbose_name = 'BTC Buy Order'
        verbose_name_plural = 'BTC Buy Orders'


class FundsTransfer(models.Model):
    """
    Represents a funds transfer request. When executed, it will be accounted
    as balance available on a Billing Account.
    """
    billing_account = models.ForeignKey('BillingAccount', related_name='funds_transfers')
    funds_transfer_state = models.CharField('state', max_length=255, choices=ORDER_STATES, default='PENDING')
    amount_brl = CryptAmount('BRL amount')

    # Audit fields
    created_at = models.DateTimeField('created at', auto_now_add=True)
    modified_at = models.DateTimeField('modified at', auto_now=True)

    class Meta:
        ordering = '-created_at',
        verbose_name = 'Funds Transfer'
        verbose_name_plural = 'Funds Transfers'

    def __str__(self):
        return '{} - BRL {} - {}'.format(
            self.billing_account.user.username,
            self.amount_brl,
            self.funds_transfer_state
        )
