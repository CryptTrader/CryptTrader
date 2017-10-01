import datetime
from decimal import Decimal

from django import test

from trader.core.models import BillingAccount, User, BTCBuyOrder, FundsTransfer, BTCSellOrder


class BillingAccountModelTest(test.TestCase):
    def setUp(self):
        today = datetime.date.today()
        self.u = User.objects.create(username='username', tax_id='1', date_of_birth=today)
        self.ba = BillingAccount.objects.create(user=self.u)

    def test_billing_account_created(self):
        """Billing account should be created."""
        self.assertTrue(BillingAccount.objects.exists())

    def test_billing_account_user_type(self):
        """User associated to Billing Account should be Crypt User."""
        self.assertIsInstance(self.ba.user, User)

    def test_billing_account_user(self):
        """Billing account should have an user."""
        self.assertEqual(self.ba.user, self.u)

    def test_has_created_at_field(self):
        """Billing Account should have datetime created_at field."""
        self.assertIsInstance(self.ba.created_at, datetime.datetime)

    def test_has_modified_at_field(self):
        """Billing Account should have datetime modified_at field."""
        self.assertIsInstance(self.ba.modified_at, datetime.datetime)

    def test_str_method(self):
        """__str__() method should display username, amount and currency."""
        expected = ['username', 'BRL', '0.0']
        with self.subTest():
            for e in expected:
                self.assertIn(e, str(self.ba))


class BillingAccountBalancesWithPendingBTCBuyOrder(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='u')
        self.ba = BillingAccount.objects.create(user=u)

        BTCBuyOrder.objects.create(
            billing_account=self.ba,
            amount_brl=10.,
            amount_btc=.5,
            type='BUYBTC'
        )

    def test_btc_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_btc, 0)


class BillingAccountBalancesWithExecutedBTCBuyOrder(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='u')
        self.ba = BillingAccount.objects.create(user=u)
        BTCBuyOrder.objects.create(
            billing_account=self.ba,
            amount_brl=10.,
            amount_btc=.5,
            order_state='EXECUTED',
            type='BUYBTC'
        )

    def test_btc_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_btc, .5)


class BillingAccountBalancesWithExecutedFundsTransfer(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='u')
        self.ba = BillingAccount.objects.create(user=u)
        FundsTransfer.objects.create(
            billing_account=self.ba,
            amount_brl=10.,
            funds_transfer_state='EXECUTED'
        )

    def test_brl_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_brl, 10.)


class BillingAccountBalancesWithAllTransfersExecuted(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='u')
        self.ba = BillingAccount.objects.create(user=u)

        FundsTransfer.objects.create(
            billing_account=self.ba,
            amount_brl=10.,
            funds_transfer_state='EXECUTED'
        )

        BTCBuyOrder.objects.create(
            billing_account=self.ba,
            amount_brl=2,
            amount_btc=.5,
            order_state='EXECUTED',
            type='BUYBTC'
        )

        BTCSellOrder.objects.create(
            billing_account=self.ba,
            amount_brl=1.5,
            amount_btc=.4,
            order_state='EXECUTED',
            type='SELLBTC'
        )

    def test_brl_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_brl, 9.5)

    def test_btc_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_btc, Decimal('0.100000'))


class BillingAccountBalancesWithExecutedAndPendingOrders(test.TestCase):
    def setUp(self):
        u = User.objects.create(username='u')
        self.ba = BillingAccount.objects.create(user=u)

        FundsTransfer.objects.create(
            billing_account=self.ba,
            amount_brl=10.,
            funds_transfer_state='EXECUTED'
        )

        BTCBuyOrder.objects.create(
            billing_account=self.ba,
            amount_brl=2,
            amount_btc=.5,
            order_state='EXECUTED',
            type='BUYBTC'
        )

        BTCSellOrder.objects.create(
            billing_account=self.ba,
            amount_brl=1.5,
            amount_btc=.4,
            order_state='EXECUTED',
            type='SELLBTC'
        )

        BTCBuyOrder.objects.create(
            billing_account=self.ba,
            amount_brl=1,
            amount_btc=.05,
            order_state='PENDING',
            type='BUYBTC'
        )

    def test_brl_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_brl, 8.5)

    def test_btc_balance(self):
        """BTC balance should be zero."""
        self.assertEqual(self.ba.balance_btc, Decimal('0.100000'))
