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

COMMON = ["it", "or", "no", "the", "a", "an", "as", "of", "is", "are", "for", "to", "%s", "`%s'", "'%s'", "not", "yes", "at", "with", "by", "in", "on", "and"]
CHARS = " !,.?;:_*"

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

                # Strip html tags.
                entry = striptags(sentence.msgid)
                # Get rid of underscores...
                entry = entry.replace("_", "")
                # ... and newline chars
                entry = entry.replace("\n", " ")
                # Strip usual ponctuation characters at end of line.
                entry = entry.strip(CHARS)
                # Splitting on spaces
                entry = entry.split(" ")

                for word in entry:
                    # More clean up
                    for char in CHARS:
                        word = word.replace(char, "")
                    if "%" in word:
                        word = ""
                    # Check for blanks
                    if not word.isspace() and len(word) > 0 and not word.isnumeric():
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
