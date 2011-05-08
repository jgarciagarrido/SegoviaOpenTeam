#!/usr/bin/python
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home/quemepongohoy.info/public_html")

# Switch to the directory of your project. (Optional.)
os.chdir("/home/quemepongohoy.info/public_html/quemepongo")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "quemepongo.settings_production"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
