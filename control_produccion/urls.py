from django.conf.urls import url

from . import views

app_name = 'control_produccion'
urlpatterns = [
    # ex: /control_produccion/
    url(r'^$', views.ProduccionView.as_view(), name='index'),
    # ex: /control_produccion/analytics/
    url(r'^analytics/$', views.AnalyticsView.as_view(), name='analytics'),
    # ex: /control_produccion/orders/
    url(r'^orders/$', views.OrdersView.as_view(), name='orders'),
    # ex: /control_produccion/clients/
    url(r'^clients/$', views.ClientsView.as_view(), name='clients'),
    # ex: /control_produccion/machines/
    url(r'^machines/$', views.MachinesView.as_view(), name='machines'),
    # ex: /control_produccion/machines/<machine-name>/
    url(r'^machines/(?P<machine>.+)/$', views.MachineDetailView.as_view(),
        name='machine_detail'),
    # ex: /control_produccion/active_orders_display/
    url(r'active_orders_display/$', views.ActiveOrdersView.as_view(),
        name='active_orders'),
    # ex: /control_produccion/active_orders_refresh/
    url(r'active_orders_refresh/$', views.ActiveOrdersRefreshView.as_view(),
        name='active_orders_refresh'),
    # ex: /control_produccion/refresh_database/
    url(r'refresh_database/$', views.ActiveOrdersView.refresh_database,
        name='refresh_database'),
    # ex: /control_produccion/orders/5/
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(),
        name='order_detail'),
]
