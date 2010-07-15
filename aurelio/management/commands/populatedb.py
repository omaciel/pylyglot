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
from bidu.aurelio.models import Sentence, Package, Word

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

CHARS = "-!,.?;:_*/()@#$%^&"

class Command(BaseCommand):

    def handle(self, *test_labels, **options):
        print settings.SCRATCH_DIR

        conffiles = glob.glob(os.path.join(settings.SCRATCH_DIR, '*.po'))

        conffiles.sort()

        for f in conffiles:
            self.populate_db(f)

    @transaction.commit_manually
    def populate_db(self, po):
        packageName = os.path.basename(po).split(".")[0]

        package, created = Package.objects.get_or_create(name=packageName)
        print "Parsing %s" % packageName
        po = pofile(po, autodetect_encoding=True, encoding='utf-8')
        valid_entries = [e for e in po if not e.obsolete]

        sentences = []

        try:
            for entry in valid_entries:
                sentence, created = Sentence.objects.get_or_create(msgid=entry.msgid, msgstr=entry.msgstr)
                if entry.flags:
                    sentence.flags = ", ".join(entry.flags)
                sentence.translated = entry.translated()
                sentence.packages.add(package)

                sentences.append(sentence)
        except Exception, e:
            print "&&&&&&&&&&&&&&&&&&&&&&&"
            print str(e)
            transaction.rollback()
        else:
            transaction.commit()

        try:
            for sentence in sentences:

                # Strip html tags...
                entry = striptags(sentence.msgid)
                # ... and other non alpha characters...
                for char in CHARS:
                    entry = entry.replace(char, "")
                # ... and newline chars
                entry = entry.replace("\n", " ")
                # Splitting on spaces
                entry = entry.split(" ")

                for word in entry:
                    # Check for blanks
                    if not word.isspace() and len(word) > 1 and not word.isdigit():
                        # Remove common articles
                        if word.lower() not in COMMON:
                            term, created = Word.objects.get_or_create(term=word.lower())
                            sentence.words.add(term)

        except Exception, e:
            print "**************************"
            print str(e)
            transaction.rollback()
        else:
            transaction.commit()
