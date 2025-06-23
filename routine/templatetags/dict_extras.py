from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.simple_tag
def dict_get_two(dict_obj, key1, key2):
    if dict_obj is None:
        return []
    return dict_obj.get((key1, key2), [])

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

#@register.filter
# def get(dictionary, key):
#     return dictionary.get(key, [])

@register.filter
def dict_get(d, key):
    return d.get(key)
