from django import template
from django.core.exceptions import ObjectDoesNotExist

from ..models import Order_Group


register = template.Library()


@register.assignment_tag
def get_order_group_in_order(order, group):
    """
    Return Order_Group instance associated with given
    Order and Group, or None if instance does not exist.
    """
    try:
        proc_group = Order_Group.objects.get(
            order=order, group=group)
    except ObjectDoesNotExist:
        return None
    return proc_group
