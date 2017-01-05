import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import (Avg, Count, ExpressionWrapper, F,
                              DecimalField, Sum)
from django.utils import timezone

from .models import Order, Order_Process, Process


class OrderController():
    @classmethod
    def get_general_top_five_most_often_present_processes(cls):
        """Return the top 5 processes more often present in Orders."""
        return Process.objects.annotate(
            Count('order_process')).order_by('-order_process__count')[:5]

    @classmethod
    def get_last_week_top_five_most_often_present_processes(cls):
        """
        Return the top 5 processes more often present in
        Orders created last week.
        """
        last_week = timezone.now() - datetime.timedelta(days=8)
        return Process.objects.filter(
            order_process__order__order_date_created__gt=last_week).annotate(
                Count('order_process')).order_by('-order_process__count')[:5]

    @classmethod
    def get_last_month_top_five_most_often_present_processes(cls):
        """
        Return the top 5 processes more often present in
        Orders created last month.
        """
        last_month = timezone.now() - datetime.timedelta(days=31)
        return Process.objects.filter(
            order_process__order__order_date_created__gt=last_month).annotate(
                Count('order_process')).order_by('-order_process__count')[:5]

    @classmethod
    def get_general_top_five_most_frequent_clients(cls):
        """Return the top 5 most frequent clients in all Orders."""
        return Order.objects.values('order_client').annotate(
            Count('order_client')).order_by('-order_client__count')[:5]

    @classmethod
    def get_last_week_top_five_most_frequent_clients(cls):
        """
        Return the top 5 most frequent clients in all Orders
        created last week.
        """
        last_week = timezone.now() - datetime.timedelta(days=8)
        return Order.objects.filter(
            order_date_created__gt=last_week).values('order_client').annotate(
                Count('order_client')).order_by('-order_client__count')[:5]

    @classmethod
    def get_last_month_top_five_most_frequent_clients(cls):
        """
        Return the top 5 most frequent clients in all Orders
        created last month.
        """
        last_month = timezone.now() - datetime.timedelta(days=31)
        return Order.objects.filter(
            order_date_created__gt=last_month).values('order_client').annotate(
                Count('order_client')).order_by('-order_client__count')[:5]
