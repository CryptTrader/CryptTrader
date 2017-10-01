import datetime

from django import test

from trader.core.models import User


class UserModelTest(test.TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.u = User.objects.create(username='u', tax_id='1', date_of_birth=self.today)

    def test_user_tax_id_type(self):
        """User should have Tax ID field as string."""
        self.assertIsInstance(self.u.tax_id, str)

    def test_user_tax_id_value(self):
        """User tax ID value must match."""
        self.assertEqual(self.u.tax_id, '1')

    def test_user_dob_type(self):
        """User date of birth should be a date."""
        self.assertIsInstance(self.u.date_of_birth, datetime.date)

    def test_user_dob_value(self):
        """User DOB should match."""
        self.assertEqual(self.u.date_of_birth, self.today)

    def test_str_method(self):
        """__str__() method should display username."""
        self.assertIn('u', str(self.u))
