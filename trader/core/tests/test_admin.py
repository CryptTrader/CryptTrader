from django import test

from trader.core.admin import admin, BTCOrderModelAdmin, execute_order, cancel_order
from trader.core.models import BTCOrder, User, BillingAccount


class BTCOrderModelAdminTest(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='username')
        ba = BillingAccount.objects.create(user=u)
        BTCOrder.objects.create(billing_account=ba, amount_brl=1., amount_btc=1.)

        self.model_admin = BTCOrderModelAdmin(BTCOrder, admin.site)

    def test_has_action_execute_order(self):
        """ModelAdmin should have execute_order action."""
        self.assertIn(execute_order, self.model_admin.actions)

    def test_has_action_cancel_order(self):
        """ModelAdmin should have execute_order action."""
        self.assertIn(cancel_order, self.model_admin.actions)
