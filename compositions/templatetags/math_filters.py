from django import template
from decimal import Decimal, ROUND_DOWN
from django.contrib.humanize.templatetags.humanize import intcomma
register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 'N/A'


@register.filter
def multiplymoney(value, arg):
    try:
        result = Decimal(value) * Decimal(arg)
        return result.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    except (ValueError, TypeError, InvalidOperation):
        return 'N/A'


@register.filter(name='trim')
def trim(value):
    """Removes leading and trailing whitespace from a string."""
    return value.strip()


@register.filter(name='suppress_trailing_zeros')
def suppress_trailing_zeros(value):
    if isinstance(value, Decimal):
        value = value.normalize()

        if value % 1 == 0:  # It's essentially an integer
            return f"{int(value)},00"
        
        value_str = str(value)
        whole, decimal = value_str.split(".")
        # Make sure to keep significant decimals
        return f"{whole},{decimal}"

    elif isinstance(value, (float, int)):
        value = Decimal(str(value)).normalize()

        if value % 1 == 0:  # It's essentially an integer
            return f"{int(value)},00"

        value_str = str(value)
        whole, decimal = value_str.split(".")
        # Make sure to keep significant decimals
        return f"{whole},{decimal}"

    else:
        return value


@register.filter(name='brazilian_currency')
def brazilian_currency(value):
    value = round(float(value), 2)  # Ensure the value has two decimal places
    value = f"{value:,.2f}"  # Format with comma as the thousands separator
    return value.replace(",", "X").replace(".", ",").replace("X", ".")