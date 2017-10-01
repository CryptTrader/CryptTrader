import datetime

from django import test

from trader.core.models import User, BillingAccount, BTCOrder


class BTCOrderTestCase(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='username')
        ba = BillingAccount.objects.create(user=u)
        self.order = BTCOrder.objects.create(billing_account=ba, amount_brl=10., amount_btc=.5)

    def test_order_created(self):
        """Order should be created."""
        self.assertTrue(BTCOrder.objects.exists())

    def test_order_btc_amount_type(self):
        """Order BTC amount should be a decimal."""
        self.assertIsInstance(self.order.amount_btc, float)

    def test_order_brl_amount_type(self):
        """Order BRL amount should be a decimal."""
        self.assertIsInstance(self.order.amount_brl, float)

    def test_order_btc_amount_value(self):
        """Order BTC amount should be near 0.5."""
        self.assertAlmostEqual(self.order.amount_btc, 0.5)

    def test_order_brl_amount_value(self):
        """Order BRL amount should be near 10."""
        self.assertAlmostEqual(self.order.amount_brl, 10.)

    def test_order_state_default_value(self):
        """Order default state should be PENDING."""
        self.assertEqual(self.order.order_state, 'PENDING')

    def test_order_has_type(self):
        """Order should contain str type."""
        self.assertIsInstance(self.order.type, str)

    def test_order_default_type(self):
        """Default type of order should be BUYBTC."""
        self.assertEqual(self.order.type, "BUYBTC")

    def test_has_created_at_field(self):
        """Order should have datetime created_at field."""
        self.assertIsInstance(self.order.created_at, datetime.datetime)

    def test_has_modified_at_field(self):
        """Order should have datetime modified_at field."""
        self.assertIsInstance(self.order.modified_at, datetime.datetime)

    def test_exchange_rate(self):
        """Exchange rate should be BRL / BTC."""
        self.assertEqual(self.order.exchange_rate, 20)

    def test_str_method(self):
        """__str__() method should display username, amount and currency."""
        expected = ['username', 'BRL', '10.0', '0.5', 'PENDING']
        with self.subTest():
            for e in expected:
                self.assertIn(e, str(self.order))
