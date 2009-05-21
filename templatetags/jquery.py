from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def jquery_script(version="1.3", minified=False, ajax_api=False):
    if ajax_api:
        return '<script src="/jq-media/jquery/%s/jquery.js" type="text/javascript"></script>' % version
    else:
        return '<script src="http://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.js" type="text/javascript"></script>' % version
