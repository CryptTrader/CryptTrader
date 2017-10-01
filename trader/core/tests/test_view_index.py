from django import test
from django.shortcuts import resolve_url as r

from trader.core.models import BTCOrder


class IndexViewTest(test.TestCase):
    def setUp(self):
        self.r = self.client.get(r('core:index'))

    def test_status_code(self):
        """Status code should be 200."""
        self.assertEqual(self.r.status_code, 200)

    def test_template_rendered(self):
        """/ should render index.html."""
        self.assertTemplateUsed(self.r, 'index.html')

    def test_template_has_html(self):
        """Template should contain HTML code."""
        self.assertContains(self.r, '<html')

    def test_template_has_panels(self):
        """Index has offers and actions panels."""
        expected = ['<h1>Painel de ofertas</h1>', '<h1>Menu</h1>']
        with self.subTest():
            for exp in expected:
                self.assertContains(self.r, exp)

    def test_template_has_context(self):
        """Index should have context variables: sell_offers and buy_offers."""
        expected = 'sell_orders', 'buy_orders'
        with self.subTest():
            for exp in expected:
                self.assertIn(exp, self.r.context)

    def test_template_orders_type(self):
        """Orders should be of type BTCOrder."""
        expected = 'sell_orders', 'buy_orders'
        with self.subTest():
            for exp in expected:
                self.assertEqual(self.r.context[exp].model, BTCOrder)

    def test_offer_panels(self):
        """Template should have BUY and SELL panels."""
        expected = '<h2>Compra</h2>', '<h2>Venda</h2>'
        with self.subTest():
            for exp in expected:
                self.assertContains(self.r, exp, 1)
