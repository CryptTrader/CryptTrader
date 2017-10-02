from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url as r

from trader.core.forms import BTCSellOrderForm, BTCBuyOrderForm
from trader.core.models import BTCOrder


@login_required
def index(request):
    sell_orders = BTCOrder.objects.filter(order_state='PENDING', type='SELLBTC')
    buy_orders = BTCOrder.objects.filter(order_state='PENDING', type='BUYBTC')
    return render(request, 'index.html', {
        'sell_orders': sell_orders,
        'buy_orders': buy_orders,
        'sell_order_form': BTCSellOrderForm(),
        'buy_order_form': BTCBuyOrderForm()
    })


def create_order(form, user, type):
    new_order = form.save(commit=False)
    new_order.billing_account = user.billing_account
    new_order.type = type
    new_order.save()


@login_required
def sell_order(request):
    if request.method == 'POST':
        form = BTCSellOrderForm(request.POST)
        if form.is_valid():
            create_order(form, request.user, 'SELLBTC')
            return redirect(r('core:index'))
    return redirect(r('core:index'))


@login_required
def buy_order(request):
    if request.method == 'POST':
        form = BTCSellOrderForm(request.POST)
        if form.is_valid():
            create_order(form, request.user, 'BUYBTC')
            return redirect(r('core:index'))
    return redirect(r('core:index'))
