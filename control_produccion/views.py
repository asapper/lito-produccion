from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponse


from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import (Order, Group, Process, Order_Group,
                     Order_Process, ProcessState)
from .utility import OrderController
from .db_utility import DatabaseController
from .db_utility import (VALUE_ORDER_DB_ID, VALUE_PRODUCT_ID,
                         VALUE_PROCESS_GROUP, VALUE_PROCESS_ID,
                         VALUE_PROCESS_NAME, VALUE_OP_NUMBER, VALUE_CLIENT,
                         VALUE_DESCRIPTION, VALUE_PRODUCT_NAME, VALUE_QUANTITY,
                         VALUE_SHEETS, VALUE_DATE_CREATED, VALUE_DUE_DATE)


class ActiveOrdersRefreshView(ListView):
    template_name = 'control_produccion/active_orders_table.html'
    context_object_name = 'latest_active_orders_list'

    def get_context_data(self, **kwargs):
        """Add process list to context and return context data."""
        context = super(ActiveOrdersRefreshView, self).get_context_data(
            **kwargs)
        groups = Group.objects.all().order_by('group_sh_id')
        context['group_list'] = groups
        return context

    def get_queryset(self):
        """Return all active Orders."""
        return Order.objects.filter(
            order_is_finished=False).order_by('order_op_number')


class ActiveOrdersView(TemplateView):
    template_name = 'control_produccion/active_orders.html'

    def refresh_processes_data(self):
        """
        Connect to Sunhiv db and update data on the processes
        of all unfinished orders. Finish the ones whose updated
        data indicates they have been finished.
        """
        # get all order_group instances
        order_groups = Order_Group.objects.filter(
            order__order_is_finished=False)
        for order_group in order_groups:
            if order_group.get_is_finished() is True:
                order.set_finished()
        # get all unfinished order_process instances
        order_processes = Order_Process.objects.filter(
            order__order_is_finished=False)
        # query Sunhive db
        for order_process in order_processes:
            state = DatabaseController.get_process_data(
                order_process.order.get_op_number(),
                order_process.order.get_product_number(),
                order_process.process.group_sh_id,
                order_process.process.process_sh_id)
            # if state is started, mark order_process as started
            if state == ProcessState.STARTED:
                if order_process.get_is_started() is False:
                    order_process.set_started()
            # if state is finished, mark order_process as finished
            elif state == ProcessState.FINISHED:
                if order_process.get_is_finished() is False:
                    order_process.set_finished()
            # if state is not started, do nothing
            else:
                pass
        return HttpResponse()

    def refresh_database(self):
        """Connect to Sunhive db and update records on Active Orders."""
        # query Sunhive db
        try:
            results = DatabaseController.get_orders()
        except DatabaseError:  # if not able to connect to Sunhive db
            return HttpResponse()
        # create objects based on result from query
        for item in results:
            try:  # retrieve order
                order = Order.objects.get(
                    order_op_number=item[VALUE_OP_NUMBER])
            except ObjectDoesNotExist:  # create Order instance
                # create order instance
                order = Order.objects.create(
                    order_sh_id=item[VALUE_ORDER_DB_ID],
                    order_op_number=item[VALUE_OP_NUMBER],
                    order_client=item[VALUE_CLIENT],
                    order_quantity=item[VALUE_QUANTITY],
                    order_total_sheets=item[VALUE_SHEETS],
                    order_description=item[VALUE_DESCRIPTION],
                    order_product_number=item[VALUE_PRODUCT_ID],
                    order_product_name=item[VALUE_PRODUCT_NAME],
                    order_date_created=item[VALUE_DATE_CREATED],
                    order_due_date=item[VALUE_DUE_DATE])
            try:
                # get group
                group = Group.objects.get(
                    group_sh_id=item[VALUE_PROCESS_GROUP])
            except ObjectDoesNotExist:
                # create group
                group = Group.objects.create(
                    group_sh_id=item[VALUE_PROCESS_GROUP],
                    group_name="Grupo {}".format(
                        item[VALUE_PROCESS_GROUP]))
            # get/create Order Group instance
            order_group_instance = Order_Group.objects.get_or_create(
                order=order, group=group)
            # get/create Process instance
            try:
                process = Process.objects.get(process_name=item[VALUE_PROCESS_NAME])
            except ObjectDoesNotExist:
                process = Process.objects.create(
                    process_sh_id=item[VALUE_PROCESS_ID],
                    group_sh_id=item[VALUE_PROCESS_GROUP],
                    process_name=item[VALUE_PROCESS_NAME])
            # get/create Group Process instance
            try:
                Order_Process.objects.get(order=order, process=process)
            except ObjectDoesNotExist:
                Order_Process.objects.create(order=order, process=process)
        return HttpResponse()


class ProduccionView(TemplateView):
    template_name = 'control_produccion/index.html'


class AnalyticsView(TemplateView):
    template_name = 'control_produccion/analytics.html'

    def get_general_top_most_present_processes(self):
        """
        Call utility function to get the top 5 process
        most often seen in all the Orders.
        """
        return OrderController.get_general_top_five_most_often_present_processes()

    def get_last_week_top_most_present_processes(self):
        """
        Call utility function to get the top 5 process
        most often seen in Orders created last week.
        """
        return OrderController.get_last_week_top_five_most_often_present_processes()

    def get_last_month_top_most_present_processes(self):
        """
        Call utility function to get the top 5 process
        most often seen in Orders created last month.
        """
        return OrderController.get_last_month_top_five_most_often_present_processes()

    def get_general_top_most_frequent_clients(self):
        """
        Call utility function to get the top 5 most
        frequent clients in all orders.
        """
        return OrderController.get_general_top_five_most_frequent_clients()
    
    def get_last_week_top_most_frequent_clients(self):
        """
        Call utility function to get the top 5 most
        frequent clients in Orders created last week.
        """
        return OrderController.get_last_week_top_five_most_frequent_clients()

    def get_last_month_top_most_frequent_clients(self):
        """
        Call utility function to get the top 5 most
        frequent clients in Orders created last month.
        """
        return OrderController.get_last_month_top_five_most_frequent_clients()
