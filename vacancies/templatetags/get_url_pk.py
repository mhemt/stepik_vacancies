from django import template

register = template.Library()


@register.filter()
def get_url_pk(url: str):
    for element in url.split('/'):
        if element.isnumeric():
            return element
