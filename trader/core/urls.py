from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sell-order$', views.sell_order, name='sell-order'),
    url(r'^buy-order$', views.buy_order, name='buy-order')
]
