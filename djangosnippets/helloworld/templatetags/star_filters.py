from django import template

register = template.Library()

@register.filter
def rating_to_percent(value):
    try:
        return float(value) / 5 * 100
    except:
        return 0