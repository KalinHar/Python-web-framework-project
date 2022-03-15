from django import template

register = template.Library()


@register.simple_tag
def profile_is(user):

    if not user.is_authenticated:
        return None
    elif user.groups.filter(name='casher').exists():
        return 'casher'
    elif user.groups.filter(name='reporter').exists():
        return 'reporter'
    elif user.groups.filter(name='clients').exists():
        return 'client'
    else:
        return 'guest'


@register.simple_tag
def sum_of(diff, price, tax):
    result = f'{(diff * price + tax):.2f}'
    return result


@register.simple_tag
def diff_of(a, b):
    result = a - b
    return result


@register.simple_tag
def row_color(paid):
    if paid:
        return 'alert-success'
    return 'alert-warning'


@register.simple_tag
def is_client(client, user):
    if client == user:
        return True
    return False
