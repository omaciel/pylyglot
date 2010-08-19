# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

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

from bidu.core.models import Sentence, Word
from bidu.packages.models import Package
from bidu.languages.models import Language
from bidu.translations.models import Translation

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

CHARS = "-!,.?;:_*/()@#$%^&'"

class Command(BaseCommand):

    def handle(self, *test_labels, **options):
        logging.info("Scratch directory is %s." % settings.SCRATCH_DIR)

        conffiles = glob.glob(os.path.join(settings.SCRATCH_DIR, '*.po'))

        conffiles.sort()

        for f in conffiles:
            self.populate_db(f)

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
            revisiondate = datetime.strptime(revisiondate.astimezone(tzutc()).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        except Exception, e:
            logging.info("Package %s doesn't seem to be translated yet for %s." % (packageName, language))
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
                    sentence, created = Sentence.objects.get_or_create(msgid=entry.msgid)
                    if entry.flags:
                        sentence.flags = ", ".join(entry.flags)

                    # Add translation
                    translation, created = Translation.objects.get_or_create(msgstr=entry.msgstr, language=language, package=package)
                    translation.translated = entry.translated()
                    if created or revisiondate > translation.revisiondate:
                        translation.revisiondate = revisiondate
                    translation.save()
                    sentence.translations.add(translation)

                    # Strip html tags...
                    entry = striptags(sentence.msgid)
                    # ... and other non alpha characters...
                    for char in CHARS:
                        entry = entry.replace(char, " ")
                    # ... and double-quotes...
                    entry = entry.replace('"', " ")
                    # ... and newline chars
                    entry = entry.replace("\n", " ")
                    # Splitting on spaces
                    entry = entry.split(" ")

                    words = []
                    for word in entry:
                        # Check for blanks
                        if not word.isspace() and len(word) > 1 and not word.isdigit():
                            # Remove common articles
                            if word.lower() not in COMMON:
                                words.append(word)
                    sentence.length = len(words)
                    sentence.save()

        except Exception, e:
            logging.error("Failed to create sentences: %s" % str(e))
            transaction.rollback()
        else:
            transaction.commit()
