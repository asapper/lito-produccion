from django.conf.urls import url

from . import views

app_name = 'ventas'
urlpatterns = [
    # ex: /ventas/
    url(r'^$', views.VentasView.as_view(), name='index'),
    # ex: /ventas/orders/
    url(r'^orders/$', views.OrdersView.as_view(), name='orders'),
    # ex: /ventas/orders/5
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(),
        name='order_detail'),
    # ex: /ventas/quotes/
    url(r'^quotes/$', views.QuotesView.as_view(), name='quotes'),
    # ex: /ventas/quotes/new
    url(r'^quotes/new$', views.QuoteCreateView.as_view(),
        name='quote_create'),
    # ex: /ventas/quotes/5/
    url(r'^quotes/(?P<pk>[0-9]+)/$', views.QuoteDetailView.as_view(),
        name='quote_detail'),
    # ex: /ventas/quotes/5/edit/
    url(r'^quotes/(?P<pk>[0-9]+)/edit$', views.QuoteEditView.as_view(),
        name='quote_edit'),
    # ex: /ventas/quotes/5/authorize/
    url(r'^quotes/(?P<pk>[0-9]+)/authorize$', views.authorize_quote,
        name='quote_authorize'),
    # ex: /ventas/quotes/5/approve/
    url(r'^quotes/(?P<pk>[0-9]+)/approve$', views.OrderCreateView.as_view(),
        name='quote_approve'),
]
