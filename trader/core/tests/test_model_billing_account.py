import datetime

from django import test

from trader.core.models import BillingAccount, User


class BillingAccountModelTest(test.TestCase):
    def setUp(self):
        today = datetime.date.today()
        self.u = User.objects.create(username='u', tax_id='1', date_of_birth=today)
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
