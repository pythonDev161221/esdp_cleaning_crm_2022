from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='cash_order_count')
def cash_order_count(user):
    return user.manager_cash.filter(is_nullify=False).count()
