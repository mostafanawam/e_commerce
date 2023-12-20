from django import template
register=template.Library()


@register.filter
def multiply(val1,val2):
    try:
        return val1*val2
    except:
        return "error"

@register.filter
def sum(val1,val2):
    try:
        return val1+val2
    except:
        return "error"