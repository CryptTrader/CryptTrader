from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from trader.core.models import BTCOrder


@login_required
def index(request):
    sell_orders = BTCOrder.objects.filter(order_state='PENDING', type='SELLBTC')
    buy_orders = BTCOrder.objects.filter(order_state='PENDING', type='BUYBTC')
    return render(request, 'index.html', {
        'sell_orders': sell_orders,
        'buy_orders': buy_orders,
    })
