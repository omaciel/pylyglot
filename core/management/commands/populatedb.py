# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-
#
# This file is part of Pylyglot.
#
# Pylyglot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylyglot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pylyglot.  If not, see <http://www.gnu.org/licenses/>.

import glob
import os.path
from django.conf import settings
from django.db import transaction
from django.template.defaultfilters import striptags
from django.core.management.base import AppCommand
from django.core.management.base import BaseCommand, CommandError

from polib import pofile

from pylyglot.core.models import Language, Package, Translation
from pylyglot.core.lib import populate_db

from datetime import datetime
import logging

log = logging.getLogger()
log.setLevel(settings.LOG_LEVEL)

class Command(BaseCommand):

    def handle(self, *test_labels, **options):
        logging.info("Scratch directory is %s." % settings.SCRATCH_DIR)

        conffiles = glob.glob(os.path.join(settings.SCRATCH_DIR, '*.po'))

        conffiles.sort()

        for f in conffiles:
            t1 = datetime.now()
            self.populate_db(f)
            t2 = datetime.now()
            logging.info("Package added in %s seconds." % (t2 - t1).seconds)

    @transaction.commit_manually
    def populate_db(self, pfile):

        # Read in the *.po file
        try:
            po = pofile(pfile, autodetect_encoding=True, encoding='utf-8')
        except Exception, e:
            logging.error(str(e))
            return

        # Extract information from the file name.
        packageName = os.path.basename(pfile).split(".")[0]
        language =  os.path.basename(pfile).split(".")[-2]

        language, created = Language.objects.get_or_create(short_name=language)
        logging.info("Language %s created: %s" % (language.short_name, created))

        package, created = Package.objects.get_or_create(name=packageName)
        logging.info("Package %s created: %s" % (packageName, created))


        populate_db(po, package, language)

