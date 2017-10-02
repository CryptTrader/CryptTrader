from django import test
from django.shortcuts import resolve_url as r

from trader.core.models import User, BillingAccount, BTCSellOrder, BTCBuyOrder


class BTCSellOrderViewTest(test.TestCase):
    def setUp(self):
        u = User.objects.create_user(username='user', email='a@user.com', password='pas$4W0rd')
        self.ba = BillingAccount.objects.create(user=u)
        self.client.login(username='user', password='pas$4W0rd')
        self.resp = self.client.post(r('core:sell-order'), {'amount_brl': 2.5, 'amount_btc': 0.5})

    def test_success(self):
        """POST /sell-order should redirect to index."""
        self.assertRedirects(self.resp, r('core:index'))

    def test_order_created(self):
        """Order should be created in database."""
        self.assertTrue(BTCSellOrder.objects.exists())


class BTCBuyOrderViewTest(test.TestCase):
    def setUp(self):
        u = User.objects.create_user(username='user', email='a@user.com', password='pas$4W0rd')
        self.ba = BillingAccount.objects.create(user=u)
        self.client.login(username='user', password='pas$4W0rd')
        self.resp = self.client.post(r('core:buy-order'), {'amount_brl': 2.5, 'amount_btc': 0.5})

    def test_success(self):
        """POST /sell-order should redirect to index."""
        self.assertRedirects(self.resp, r('core:index'))

    def test_order_created(self):
        """Order should be created in database."""
        self.assertTrue(BTCBuyOrder.objects.exists())


class BTCBuyOrderViewErrorTest(test.TestCase):
    def setUp(self):
        u = User.objects.create_user(username='user', email='a@user.com', password='pas$4W0rd')
        self.ba = BillingAccount.objects.create(user=u)
        self.client.login(username='user', password='pas$4W0rd')
        self.resp = self.client.post(r('core:buy-order'), {'amount_brl': 2.5, 'amount_btc': ''})

    def test_success(self):
        """POST /sell-order should redirect to index."""
        self.assertRedirects(self.resp, r('core:index'))

    def test_order_created(self):
        """Order should be created in database."""
        self.assertFalse(BTCBuyOrder.objects.exists())