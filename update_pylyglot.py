#!/usr/bin/python
# coding: utf-8

import sys, os

path = '/home/sgtotainha/pylyglot'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pylyglot.settings'

#from core.models import *

#accer = Package.objects.get(name='accerciser')
#languages = Language.objects.all()

#for language in languages:
#       (job, created) = Job.objects.get_or_create(language=language, package=accer)
#       job.save()

from core.management.commands import populatedb
cmd = populatedb.Command()
cmd.execute()
