import os, sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)

sys.path.append(workspace)
sys.path.append('/var/www/')
sys.path.append('/var/www/lan')

#also add any third party apps to the path if needed

os.environ['DJANGO_SETTINGS_MODULE'] = 'lan.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
