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

from pylyglot.core.models import Package, Language, Sentence, Translation

import tempfile
from urllib import urlopen

import logging
import time
import os

log = logging.getLogger()
log.setLevel(settings.LOG_LEVEL)

def update_package(package):

    logging.debug("Attempting to update %s" % package)
    languages = Language.objects.all()

    for language in languages:
        try:
            url = "%s.%s.po" % (package.src_url, language.short_name)

            try:
                remote_file = urlopen(url)
            except Exception, e:
                logging.error("Failed to fetch file for %s using url %s" % (package.name, package.src_url))
                return

            (fd, filename) = tempfile.mkstemp(package.name)
            f = os.fdopen(fd, "w")

            for line in remote_file.readlines():
                f.write(line)
            f.close()

            try:
                po = pofile(filename, autodetect_encoding=True, encoding='utf-8')
            except Exception, e:
                logging.error("Failed to open po file %s for %s" % (package.name, language))
                logging.error("Error: %s" % str(e))
                return

            populate_db(po, language, package)

        except Exception, e:
            logging.error("Failed to download the file located on %s" % url)
            logging.error("Error: %s" % str(e))
            return

@transaction.commit_manually
def populate_db(po, language, package):

    logging.debug("Updating %s translations for %s" % (language.long_name, package.name))

    # Delete existing translations for this package/language combination
    #translations = Translation.objects.filter(language=language, package=package)

    #if translations:
    #    logging.info("Deleting existing translations for %s / %s." % (package.name, language.short_name))
    #    translations.delete()

    valid_entries = [e for e in po if not e.obsolete]

    try:
        for entry in valid_entries:
            if entry.translated():
                if entry.msgid_plural:
                    entry.msgstr = entry.msgstr_plural.get('0', '')
                    entry.msgstr_plural = entry.msgstr_plural.get('1', '')

                add_translation(entry, language, package)

    except Exception, e:
        logging.error("Failed to create sentences: %s" % str(e))
        transaction.rollback()
    else:
        transaction.commit()

def add_translation(entry, language, package):

    (sentence, created) = Sentence.objects.get_or_create(msgid = entry.msgid)

    sentence.length = len(entry.msgid)
    sentence.save()

    (trans, created) = Translation.objects.get_or_create(msgstr=entry.msgstr, sentence=sentence, language=language)

    if package not in trans.packages.all():
        trans.packages.add(package)

    trans.save()

    if entry.msgid_plural:
        (sentence, created) = Sentence.objects.get_or_create(msgid = entry.msgid_plural)

        sentence.length = len(entry.msgid)
        sentence.save()

        (trans, created) = Translation.objects.get_or_create(msgstr=entry.msgstr_plural, sentence=sentence, language=language)

        if package not in trans.packages.all():
            trans.packages.add(package)

        trans.save()


def add_translations(msgid, msgstr, language, package, revisiondate):

    words = msgid.split()
    clean_words = []

    for word in words:
        clean_word = "".join([x for x in word if x.isalpha()])
        if len(clean_word) > 1:
            clean_words.append(clean_word)

    translation = Translation(
            msgstr = msgstr,
            msgid = msgid,
            clean_msgid = " ".join(clean_words),
            language = language,
            package = package,
            create_date = revisiondate,
            translated=True,
        )

    if len(words) == 1:
        translation.length = len(msgid)
    else:
        translation.length = len(words) * len(msgid)

    translation.save()
