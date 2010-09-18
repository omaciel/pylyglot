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
from django.template.defaultfilters import striptags
from django.core.management.base import AppCommand
from django.core.management.base import BaseCommand, CommandError

from django.db import transaction

from polib import pofile
from dateutil.parser import parse
from dateutil.tz import tzutc

from pylyglot.core.models import Language, Package, Translation

import time
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
        po = pofile(pfile, autodetect_encoding=True, encoding='utf-8')

        # Extract information from the file name.
        packageName = os.path.basename(pfile).split(".")[0]
        language =  os.path.basename(pfile).split(".")[-2]
        # Format is 2010-04-29 15:07+0300
        revisiondate = po.metadata['PO-Revision-Date']

        try:
            revisiondate = parse(revisiondate)
            revisiondate = revisiondate.astimezone(tzutc())
            revisiondate = datetime(*time.strptime(revisiondate.astimezone(tzutc()).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")[0:6])
            #revisiondate = datetime.strptime(revisiondate.astimezone(tzutc()).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        except Exception, e:
            logging.info("Package %s doesn't seem to be translated yet for %s." % (packageName, language))
            logging.error(str(e))
            return

        logging.info("Parsing %s for %s" % (packageName, language))

        language, created = Language.objects.get_or_create(short_name=language)
        logging.info("Language %s created: %s" % (language.short_name, created))

        package, created = Package.objects.get_or_create(name=packageName)
        logging.info("Package %s created: %s" % (packageName, created))

        valid_entries = [e for e in po if not e.obsolete]

        try:
            for entry in valid_entries:
                if entry.translated():
                    if entry.msgid_plural:
                        entry.msgstr = entry.msgstr_plural.get('0', '')
                        entry.msgstr_plural = entry.msgstr_plural.get('1', '')

                        if entry.msgstr:
                            self.add_translations(entry.msgid, entry.msgstr, language, package, revisiondate)
                        if entry.msgstr_plural:
                            self.add_translations(entry.msgid_plural, entry.msgstr_plural, language, package, revisiondate)
                    else:
                        if entry.msgstr:
                            self.add_translations(entry.msgid, entry.msgstr, language, package, revisiondate)

        except Exception, e:
            logging.error("Failed to create sentences: %s" % str(e))
            transaction.rollback()
        else:
            transaction.commit()

    def add_translations(self, msgid, msgstr, language, package, revisiondate):

        translation = Translation(
                msgstr = msgstr,
                msgid = msgid,
                language = language,
                package = package,
                create_date = revisiondate,
                length = len(msgid),
                translated=True,
            )
        translation.save()
