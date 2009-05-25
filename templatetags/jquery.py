from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, normalize
from django import template
from django.conf import settings
from django_jq import settings_defaults
import cjson, re, sys

JQUERY_REMOTE_URL = getattr(settings, 'JQUERY_REMOTE_URL', settings_defaults.JQUERY_REMOTE_URL)
JQUERY_LOCAL_URL  = getattr(settings, 'JQUERY_LOCAL_URL',  settings_defaults.JQUERY_LOCAL_URL)
JQUERY_VERSIONS   = getattr(settings, 'JQUERY_VERSIONS',   settings_defaults.JQUERY_VERSIONS)

module = settings.ROOT_URLCONF.split('.')
exec "from %s import %s" % (module[0], module[1]) # A little kitten die each time you do this.

register = template.Library()
SCRIPT_TAG = '<script type="text/javascript" src="%s"></script>'

def join_url(*args):
    s = '/'.join(args)
    return re.sub(r'/+', '/', s)

class URLDict(object):
    """
    Creates a dict object containing the urls 
    with their associated name for JSON encoding.
    Author: Vincent Foley
    """
    def __init__(self):
        self.dict = None

    def urls_dict(self):
        if self.dict is None:
            self.dict = self.generate_urls_dict('/', {}, urls.urlpatterns)
        return self.dict

    def generate_urls_dict(self, root, d, patterns):
        for pattern in patterns:
            if isinstance(pattern, RegexURLResolver):
                d.update(self.generate_urls_dict(join_url(root, normalize(pattern.regex.pattern)[0][0]),
                                                 {},
                                                 pattern.url_patterns))
            elif isinstance(pattern, RegexURLPattern):
                if pattern.name:
                    s = normalize(pattern.regex.pattern)[0][0]
                    s = s.replace('(', '').replace(')s', '')
                    d[pattern.name] = join_url(root, s)
        return d

@register.simple_tag
def jquery_script(version="1.3", ajax=0):
    min = '' if settings.DEBUG else '.min'
    if ajax:
        url = JQUERY_REMOTE_URL % (version, min)
    else:
        url = JQUERY_LOCAL_URL % (version, min)
    return SCRIPT_TAG % url

@register.simple_tag
def jquery_urls():
    t = template.Template( '''
<script type="text/javascript">
(function($){
    this.urls = {{ json_urls|safe }};
    var self = this;
    $.extend({
        url: function(){
            var token, key = '';
            var view  = arguments[0];
            var out   = self.urls[view] || false;
            if (out && arguments[1]) {
                if (typeof(arguments[1]) == 'object') {
                    for (key in arguments[1]) {
                        token = '%'+key;
                        out = out.match(token) 
                            && out.replace(token, arguments[1][key]) 
                            || out + (out.match(/\?\w+\=/) ?'&':'?') + key + '=' + arguments[1][key];
                    }
                }
                else {
                    for (key = 1; key < arguments.length; key++) {
                        token = '%_'+ (key - 1);
                        if (out.match(token)) { out = out.replace(token, arguments[key]); }
                    }
                }
            }
            return out;
        }
    });
})(jQuery);
</script>''')
    return t.render(template.Context({'json_urls':
        cjson.encode(URLDict().urls_dict())}))
