from django import template

register = template.Library()


@register.filter()
def get_url_pk(url: str):
    for i in url.split('/'):
        if i.isnumeric():
            return i
