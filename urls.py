from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'(.*)', 'django.views.static.serve', {'document_root': '/home/www/wsf/contrib/django_jq/media'}),
)

