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

from pylyglot.core.models import Package, Language, Translation, Sentence, Word

import time
from datetime import datetime
import logging

log = logging.getLogger()
log.setLevel(settings.LOG_LEVEL)

COMMON = [
    "an",
    "and",
    "are",
    "as",
    "at",
    "by",
    "for",
    "in",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "yes",
]

CHARS = "[]=-!,.?;:_*/()@#$%^&'"

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
                            self.add_sentence(entry, language, package, revisiondate)
                        if entry.msgstr_plural:
                            self.add_sentence(entry, language, package, revisiondate, True)
                    else:
                        if entry.msgstr:
                            self.add_sentence(entry, language, package, revisiondate)

        except Exception, e:
            logging.error("Failed to create sentences: %s" % str(e))
            transaction.rollback()
        else:
            transaction.commit()

    def add_sentence(self, entry, language, package, revisiondate, plural=False):

        if plural:
            sentence, created = Sentence.objects.get_or_create(msgid=entry.msgid_plural)
        else:
            sentence, created = Sentence.objects.get_or_create(msgid=entry.msgid)

        if entry.flags:
            sentence.flags = ", ".join(entry.flags)

        self.add_translation(entry, sentence, language, package, revisiondate, plural)

    def add_translation(self, entry, sentence, language, package, revisiondate, plural=False):

        if plural:
            msgstr = entry.msgstr_plural
            cleaned_entry = self.strip_junk(entry.msgid_plural)
        else:
            msgstr=entry.msgstr
            cleaned_entry = self.strip_junk(entry.msgid)

        translation = Translation.objects.filter(msgstr=msgstr, msgid=sentence, language=language, package=package)

        if translation:
            translation = translation[0]
            if revisiondate > translation.revisiondate:
                translation.revisiondate = revisiondate
            else:
                logging.info("This translation is older than what's the current value.")
        else:
            translation = Translation(msgstr=msgstr, msgid=sentence, language=language, package=package)
            translation.revisiondate = revisiondate
            translation.save()


        for term in self.add_words(cleaned_entry):
            if term not in translation.words.all():
                translation.words.add(term)

        sentence.length = len(translation.words.all())
        sentence.save()

        translation.translated = entry.translated()
        translation.save()

    def strip_junk(self, sentence):
        # Strip html tags...
        entry = striptags(sentence)
        # ... and other non alpha characters...
        for char in CHARS:
            entry = entry.replace(char, " ")
        # ... and double-quotes...
        entry = entry.replace('"', " ")
        # ... and newline chars
        entry = entry.replace("\n", " ")
        # Splitting on spaces
        entry = entry.split(" ")

        return entry

    def add_words(self, entry):

        terms = []
        for word in entry:
            # Check for blanks
            if not word.isspace() and len(word) > 1 and not word.isdigit():
                # Remove common articles
                if word.lower() not in COMMON:
                    term, created = Word.objects.get_or_create(term=word.lower())
                    terms.append(term)

        return terms
