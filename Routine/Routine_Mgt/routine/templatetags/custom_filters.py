from django import template

register = template.Library()

@register.filter
def get_day_availability(weekly_availability, day):
    """
    Returns the availability for a given day from the weekly_availability dictionary.
    """
    return weekly_availability.get(day, [])
