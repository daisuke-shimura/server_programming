from django import template
register = template.Library()
@register.filter
def review_percent(value, count):
    try:
        return round((float(value) / count) * 100, 2)
    except (ZeroDivisionError, ValueError, TypeError):
        return 0