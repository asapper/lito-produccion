from django.conf.urls import url

from . import views

app_name = 'control_produccion'
urlpatterns = [
    # ex: /control_produccion/
    url(r'^$', views.ProduccionView.as_view(), name='index'),
    # ex: /control_produccion/analytics/
    url(r'^analytics/$', views.AnalyticsView.as_view(), name='analytics'),
    # ex: /control_produccion/active_orders_display/
    url(r'active_orders_display/$', views.ActiveOrdersView.as_view(),
        name='active_orders'),
    # ex: /control_produccion/active_orders_refresh/
    url(r'active_orders_refresh/$', views.ActiveOrdersRefreshView.as_view(),
        name='active_orders_refresh'),
    # ex: /control_produccion/refresh_database/
    url(r'refresh_database/$', views.ActiveOrdersView.refresh_database,
        name='refresh_database'),
    # ex: /control_produccion/refresh_procs_data/
    url(r'refresh_procs_data/$', views.ActiveOrdersView.refresh_processes_data,
        name='refresh_procs_data'),
]
