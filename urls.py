from django.conf.urls.defaults import *
import os
urlpatterns = patterns('',
    (r'(.*)', 'django.views.static.serve', {'document_root': '%s/media' % os.path.dirname(os.path.abspath(__file__))}),
)

