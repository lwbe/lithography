# taken from https://stackoverflow.com/questions/2683621/django-filefield-how-to-return-filename-only-in-template

import os

from django import template


register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.file.name)