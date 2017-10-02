from django import forms

from trader.core.models import BTCSellOrder, BTCBuyOrder


class BTCSellOrderForm(forms.ModelForm):
    class Meta:
        model = BTCSellOrder
        fields = ['amount_brl', 'amount_btc']


class BTCBuyOrderForm(forms.ModelForm):
    class Meta:
        model = BTCBuyOrder
        fields = ['amount_brl', 'amount_btc']
