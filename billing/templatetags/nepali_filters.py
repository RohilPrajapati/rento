from django import template
import nepali_datetime

register = template.Library()

@register.filter
def to_nepali_date(value):
    if value:
        print(value)
        try:
            return value.strftime("%B %Y")
        except Exception:
            return ""
    return ""
