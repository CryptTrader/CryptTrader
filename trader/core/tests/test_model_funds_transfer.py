import datetime

from django import test

from trader.core.models import User, BillingAccount, FundsTransfer


class FundsTransferTest(test.TestCase):
    def setUp(self):
        u = User.objects.create()
        ba = BillingAccount.objects.create(user=u)
        self.ft = FundsTransfer.objects.create(billing_account=ba, amount_brl=10.)

    def test_funds_transfer_created(self):
        """Funds Transfer should be created."""
        self.assertTrue(FundsTransfer.objects.exists())

    def test_funds_transfer_brl_amount_type(self):
        """Funds Transfer BRL amount should be a decimal."""
        self.assertIsInstance(self.ft.amount_brl, float)

    def test_funds_transfer_brl_amount_value(self):
        """Funds Transfer BRL amount should be near 10."""
        self.assertAlmostEqual(self.ft.amount_brl, 10.)

    def test_order_state_default_value(self):
        """Funds Transfer default state should be PENDING."""
        self.assertEqual(self.ft.funds_transfer_state, 'PENDING')

    def test_has_created_at_field(self):
        """Funds transfer should have datetime created_at field."""
        self.assertIsInstance(self.ft.created_at, datetime.datetime)

    def test_has_modified_at_field(self):
        """Funds transfer should have datetime modified_at field."""
        self.assertIsInstance(self.ft.modified_at, datetime.datetime)
