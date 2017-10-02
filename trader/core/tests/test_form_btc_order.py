from django import test

from trader.core.forms import BTCSellOrderForm, BTCBuyOrderForm


class BTCSellOrderModelFormTest(test.TestCase):
    def test_form_has_fields(self):
        """Form should have 2 fields."""
        form = BTCSellOrderForm()
        expected = 'amount_brl', 'amount_btc'
        self.assertSequenceEqual(expected, list(form.fields))


class BTCBuyOrderModelFormTest(test.TestCase):
    def test_form_has_fields(self):
        """Form should have 2 fields."""
        form = BTCBuyOrderForm()
        expected = 'amount_brl', 'amount_btc'
        self.assertSequenceEqual(expected, list(form.fields))
