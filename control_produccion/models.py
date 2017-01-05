from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from enum import Enum


class ProcessState(Enum):
    """
    Class used to differentiate process states.
    Any unique values would work.
    """
    NOT_STARTED = 1
    STARTED = 2
    FINISHED = 3


class Process(models.Model):
    # sunhive id
    process_sh_id = models.PositiveSmallIntegerField()
    # group id
    group_sh_id = models.PositiveSmallIntegerField()
    # name
    process_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return a string representation of this Process."""
        return self.process_name

    def get_name(self):
        """Return this Process' name."""
        return self.process_name


class Group(models.Model):
    # group id
    group_sh_id = models.PositiveSmallIntegerField(primary_key=True)
    # group name
    group_name = models.CharField(max_length=50)

    def __str__(self):
        """Return a string representation of this Process Group."""
        return self.group_name


class Order(models.Model):
    # sunhive id
    order_sh_id = models.PositiveSmallIntegerField()
    # OP number
    order_op_number = models.CharField(max_length=10)
    # client
    order_client = models.CharField(max_length=255)
    # material description
    order_description = models.CharField(max_length=100)
    # order product number
    order_product_number = models.CharField(max_length=5)
    # order product name
    order_product_name = models.CharField(max_length=100)
    # quantity
    order_quantity = models.PositiveIntegerField()
    # total sheets
    order_total_sheets = models.PositiveSmallIntegerField()
    # processes
    processes = models.ManyToManyField(Process, through="Order_Process")
    # groups
    groups = models.ManyToManyField(Group, through="Order_Group")
    # is finished?
    order_is_finished = models.BooleanField(default=False)
    # due date
    order_due_date = models.DateTimeField()
    # date created
    order_date_created = models.DateTimeField()

    def __str__(self):
        """Return a string representation of this Order."""
        return "OP: {}; Cliente: {}; Descripción: {}".format(
            self.order_op_number,
            self.order_client,
            self.order_description)

    def get_op_product_number(self):
        """Return OP number plus product number appended."""
        return "{}-{}".format(
            self.order_op_number,
            self.order_product_number)

    def get_op_number(self):
        """Return OP number."""
        return self.order_op_number

    def get_product_number(self):
        """Return product number."""
        return self.order_product_number

    def get_groups(self):
        """Return this Order's groups."""
        return self.groups.all()

    def get_processes(self):
        """Return this Order's processes."""
        return self.processes.all()

    def get_is_finished(self):
        """Return True if this Order is finished, False otherwise."""
        return self.order_is_finished

    def set_finished(self):
        """Assign this Order's is_finished to True."""
        self.order_is_finished = True
        self.save()

    def get_quantity(self):
        """Return this Order's quantity."""
        return self.order_quantity

    def is_past_due(self):
        """
        Return True is order was due in the past, return False otherwise.
        """
        return self.order_due_date.date() < timezone.now().date()

    def is_due_today(self):
        """Return True if order is due today, return False otherwise."""
        return self.order_due_date.date() == timezone.now().date()

 
class Order_Group(models.Model):
    # orders
    order = models.ForeignKey(Order)
    # group
    group = models.ForeignKey(
        Group, to_field='group_sh_id')

    def get_is_started(self):
        """
        Return True if any of the Processes associated with
        this Group are started.
        """
        # get processes associated with order
        processes = self.order.processes.filter(
            group_sh_id=self.group.group_sh_id)
        order = self.order
        # verify if any of the processes is started
        for process in processes:
            o_proc = Order_Process.objects.get(
                order=order, process=process)
            if o_proc.get_is_started() is True:
                return True
        return False

    def get_is_finished(self):
        """
        Return False if any of the Processes associated with
        this Group are not finished.
        """
        # get processes associated with order
        processes = self.order.processes.filter(
            group_sh_id=self.group.group_sh_id)
        order = self.order
        # verify if any of the processes is not finished
        for process in processes:
            o_proc = Order_Process.objects.get(
                order=order, process=process)
            if o_proc.get_is_finished() is False:
                return False
        return True


class Order_Process(models.Model):
    # order reference
    order = models.ForeignKey(Order)
    # process reference
    process = models.ForeignKey(Process)
    # is started?
    order_process_is_started = models.BooleanField(default=False)
    # is finished?
    order_process_is_finished = models.BooleanField(default=False)

    def get_op_number(self):
        """Return OP number of associated order."""
        return self.order.get_op_process_number()

    def get_is_started(self):
        """Return True if this Process is started, False otherwise."""
        return self.order_process_is_started

    def set_started(self):
        """
        Assign this Process as started by setting
        its start datetime to timezone.now.
        """
        self.order_process_is_started = True
        self.save()

    def get_is_finished(self):
        """Return True if this Process is finished, False otherwise."""
        return self.order_process_is_finished

    def set_finished(self):
        """
        Assign this Process as finished by setting
        its start datetime to timezone.now.
        """
        self.order_process_is_finished = True
        self.save()

    def get_order_quantity(self):
        """Return the quantity stored in associated Order."""
        return self.order.get_quantity()

    def get_process_name(self):
        """Return the name of the associated Process."""
        return self.process.get_name()
