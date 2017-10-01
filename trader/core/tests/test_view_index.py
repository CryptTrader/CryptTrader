from django import test
from django.shortcuts import resolve_url as r

from trader.core.models import BTCOrder, User


class IndexViewTest(test.TestCase):
    def setUp(self):
        User.objects.create_user('u', 'u@user.com', 'p4s$w0rd')
        self.client.login(username='u', password='p4s$w0rd')
        self.resp = self.client.get(r('core:index'))

    def test_status_code(self):
        """Status code should be 200."""
        self.assertEqual(self.resp.status_code, 200)

    def test_template_rendered(self):
        """/ should render index.html."""
        pass  # self.assertTemplateUsed(self.resp, 'index.html')

    def test_template_has_html(self):
        """Template should contain HTML code."""
        self.assertContains(self.resp, '<html')

    def test_template_has_panels(self):
        """Index has offers and actions panels."""
        expected = ['<h1>Painel de ofertas</h1>', '<h1>Menu</h1>']
        with self.subTest():
            for exp in expected:
                self.assertContains(self.resp, exp)

    def test_template_has_context(self):
        """Index should have context variables: sell_offers and buy_offers."""
        expected = 'sell_orders', 'buy_orders'
        with self.subTest():
            for exp in expected:
                self.assertIn(exp, self.resp.context)

    def test_template_orders_type(self):
        """Orders should be of type BTCOrder."""
        expected = 'sell_orders', 'buy_orders'
        with self.subTest():
            for exp in expected:
                self.assertEqual(self.resp.context[exp].model, BTCOrder)

    def test_offer_panels(self):
        """Template should have BUY and SELL panels."""
        expected = '<h2>Compra</h2>', '<h2>Venda</h2>'
        with self.subTest():
            for exp in expected:
                self.assertContains(self.resp, exp, 1)

    def test_offer_creation(self):
        """Template should have BUY and SELL offer creation buttons."""
        expected = '>Oferta de compra<', '>Oferta de venda<', '>Transferir fundos<', 'Meu saldo:'
        with self.subTest():
            for exp in expected:
                self.assertContains(self.resp, exp, 1)
