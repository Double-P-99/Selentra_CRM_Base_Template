"""Custom template tags and filters for the CRM."""

from django import template

register = template.Library()


@register.filter
def dict_key(d, key):
    """Look up a key in a dictionary. Usage: {{ my_dict|dict_key:key_var }}"""
    return d.get(key, [])


@register.filter
def currency_symbol(currency_code):
    """Return currency symbol for a given code."""
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'MXN': '$', 'BRL': 'R$', 'ARS': '$', 'COP': '$'}
    return symbols.get(currency_code, currency_code)
