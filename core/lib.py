# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
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

from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzutc
from django.conf import settings
from django.db import transaction
from polib import pofile
from pylyglot.core.models import Package, Language, Translation
import logging
import time

log = logging.getLogger()
log.setLevel(settings.LOG_LEVEL)

@transaction.commit_manually
def populate_db(pofile, package, language):

    # Format is 2010-04-29 15:07+0300
    # Instead of using the file's revision date, use today's date
    revisiondate = datetime.now(tzutc()).strftime("%Y-%m-%d %H:%M%Z")
    logging.info("revisiondate: %s" % revisiondate)

    try:
        revisiondate = parse(revisiondate)
        revisiondate = revisiondate.astimezone(tzutc())
        revisiondate = datetime(*time.strptime(revisiondate.astimezone(tzutc()).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")[0:6])
        #revisiondate = datetime.strptime(revisiondate.astimezone(tzutc()).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
    except Exception, e:
        logging.info("Package %s doesn't seem to be translated yet for %s." % (package.name, language.short_name))
        logging.error(str(e))
        transaction.rollback()
        return

    logging.info("Parsing %s for %s" % (package.name, language.short_name))

    """
    # Delete existing translations for this package/language combination
    translations = Translation.objects.filter(language=language, package=package)

    if translations:
        logging.info("Deleting existing translations for %s / %s." % (package.name, language.short_name))
        translations.delete()
    """

    valid_entries = [e for e in pofile if not e.obsolete]

    try:
        for entry in valid_entries:
            if entry.translated():
                if entry.msgid_plural:
                    entry.msgstr = entry.msgstr_plural.get('0', '')
                    entry.msgstr_plural = entry.msgstr_plural.get('1', '')

                    if entry.msgstr:
                        add_translations(entry.msgid, entry.msgstr, language, package, revisiondate)
                    if entry.msgstr_plural:
                        add_translations(entry.msgid_plural, entry.msgstr_plural, language, package, revisiondate)
                else:
                    if entry.msgstr:
                        add_translations(entry.msgid, entry.msgstr, language, package, revisiondate)

    except Exception, e:
        logging.error("Failed to create sentences: %s" % str(e))
        transaction.rollback()
    else:
        transaction.commit()

def add_translations(msgid, msgstr, language, package, revisiondate):

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
