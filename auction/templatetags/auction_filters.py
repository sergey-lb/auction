from django import template

register = template.Library()


@register.filter(name='auction_end_date')
def auction_end_date(value):
    value
    if isinstance(value, str):
        return value
    return value.strftime('%Y-%m-%d %H:%M')
