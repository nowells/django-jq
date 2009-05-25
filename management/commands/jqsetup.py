"""
Management utility to setup django_jq.
"""

import os, urllib

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django_jq import settings_defaults

JQUERY_VERSIONS   = getattr(settings, 'JQUERY_VERSIONS',   settings_defaults.JQUERY_VERSIONS)
JQUERY_REMOTE_URL = getattr(settings, 'JQUERY_REMOTE_URL', settings_defaults.JQUERY_REMOTE_URL)

def get_and_save(src, dst):
    print "CACHING: %s -> %s" % (src, dst)
    sock = urllib.urlopen(src)
    buff = sock.read()
    dir  = os.path.dirname(dst)
    if not os.path.exists(dir):
        os.makedirs(dir)

    file = open(dst,'wb')
    file.write(buff)
    file.close


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--onlyversion', dest='onlyversion', default=None,
            help='Setup only for specified version.'),
    )
    help = 'Used to setup django_jq.'

    def handle(self, *args, **options):
        onlyversion = options.get('onlyversion', None)
        
        # Do quick and dirty validation if --noinput
        if onlyversion:
            versions = [onlyversion]
        else:
            versions = JQUERY_VERSIONS

        path = os.path.realpath("%s/../../media/jquery/" % os.path.dirname(os.path.abspath(__file__)))
        
        for version in versions:
            get_and_save(JQUERY_REMOTE_URL % (version, ''), os.path.join(path, version, 'jquery.js'))
            get_and_save(JQUERY_REMOTE_URL % (version, '.min'), os.path.join(path, version, 'jquery.min.js'))
