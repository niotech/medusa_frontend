# bgsos/catalog/templatetags/custom_filters.py
import os
import requests
from django import template
from django.conf import settings
import math

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def subtract(value, arg):
    """Subtracts the arg from the value and formats the result to two decimal places."""
    try:
        result = float(value) - float(arg)
        return f"{result:.2f}"  # Format to two decimal places
    except (ValueError, TypeError):
        return "0.00"  # Default to "0.00" if there's an error
    
@register.filter
def cents_to_dollars(value):
    try:
        return value / 100
    except (ValueError, TypeError):
        return value


@register.filter
def divisibleby(value, divisor):
    try:
        return value / divisor
    except (ValueError, ZeroDivisionError, TypeError):
        return value

@register.filter
def format_float(value):
    return f"{value:.2f}"

@register.filter
def cents_to_points(value):
    try:
        return value / 10000
    except (ValueError, TypeError):
        return value

@register.filter
def round_up(value):
    """Rounds up the value to the nearest whole number."""
    try:
        return math.ceil(float(value))
    except (ValueError, TypeError):
        return value  # Return the original value if an error occurs
    
@register.filter(name='strip_at')
def strip_at(value):
    """
    Strip everything after and including '@' from the string.
    """
    if '@' in value:
        return value.split('@')[0]
    return value


@register.filter(name='strip_tg')
def strip_tg(value):
    """
    Strip '@tg.com' from the end of the string if it exists.
    """
    suffix = '@tg.com'
    if value.endswith(suffix):
        return value[:-len(suffix)]
    return value

@register.filter
def strip_tg_prof(email):
    """
    Strips '@tg.com' from the email address if it exists.
    """
    if email and '@tg.com' in email:
        return email.replace('@tg.com', '')
    return email

@register.filter
def cache_image(url):
    from web.services.services import MedusaStore

    medusa_store = MedusaStore()


    filename = url.split('/')[-1]
    local_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    
    if not os.path.exists(local_path):
        response = medusa_store.session.get(url, stream=True)
        if response.status_code == 200:
            
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Simpan gambar di server lokal
            with open(local_path, 'wb') as out_file:
                out_file.write(response.content)
    
    return os.path.join(settings.MEDIA_URL, 'images', filename)


@register.filter
def price_info(product):
    """ collect all prices with specified currency """
    from web.models import SiteSettings

    site_settings = SiteSettings.objects.last()

    prices = []

    for variant in product['variants']:
        for price in variant['prices']:
            if price['currency_code'] == site_settings.currency_code:
                prices.append(price['amount'])

    if not len(prices):
        return ''

    if len(prices) == 1:
        price = format_float(cents_to_dollars(prices[0]))
        return f"{site_settings.currency_symbol}{price}"

    prices.sort()

    if prices[0] == prices[-1]:
        price = format_float(cents_to_dollars(prices[0]))
        return f"{site_settings.currency_symbol}{price}"
    price1 = int(cents_to_dollars(prices[0]))
    price2 = int(cents_to_dollars(prices[-1]))
    return f"FROM {site_settings.currency_symbol}{price1}" # f"{site_settings.currency_symbol}{price1} - {site_settings.currency_symbol}{price2}"


