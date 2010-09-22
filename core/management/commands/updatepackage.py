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

from django.conf import settings
from django.core.management.base import AppCommand
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from polib import pofile

from pylyglot.core.models import Language, Package
from pylyglot.core.lib import populate_db

import logging
import tempfile
from urllib import urlopen

log = logging.getLogger()
log.setLevel(settings.LOG_LEVEL)

class Command(BaseCommand):
    args = ''

    def handle(self, *test_labels, **options):
        print test_labels

    @transaction.commit_manually
    def update_package(self, package, language, url):

        db_package, created = Package.objects.get_or_create(name=package)
        db_language, created = Language.objects.get_or_create(short_name=language)

        try:
            remote_file = urlopen(url)

            (fd, filename) = tempfile.mkstemp(package)
            f = os.fdopen(fd, "w")

            for line in remote_file.readlines():
                f.write(line)
            f.close()

            try:
                po = pofile(filename, autodetect_encoding=True, encoding='utf-8')
            except Exception, e:
                logging.error("Failed to open po file %s for %s" % (package, language))
                logging.error("Error: %s" % str(e))
                return

            populate_db(po, db_package, db_language)

        except Exception, e:
            logging.error("Failed to download the file located on %s" % url)
            logging.error("Error: %s" % str(e))
            return
