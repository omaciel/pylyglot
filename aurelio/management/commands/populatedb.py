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
from bidu.aurelio.models import Sentence, Package, Word, Language, Translation

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

CHARS = "-!,.?;:_*/()@#$%^&"

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
        language =  os.path.basename(pfile).split(".")[2]
        # Format is 2010-04-29 15:07+0300
        revisiondate = po.metadata['PO-Revision-Date'][:-5]

        try:
            revisiondate = datetime.strptime(revisiondate, "%Y-%m-%d %H:%M")
        except Exception, e:
            logging.info("Package %s doesn't seem to be translated yet for %s." % (packageName, language))
            return

        logging.info("Parsing %s for %s") % (packageName, language)

        language, created = Language.objects.get_or_create(short_name=language)
        package = Package.objects.filter(name=packageName).filter(sentence__translations__language__short_name=language.short_name).distinct()

        # Existing package?
        if package:
            package = package[0]
            # Is the *.po older or equal to existing package?
            if revisiondate == package.revisiondate or revisiondate < package.revisiondate:
                logging.info("Package %s for %s has already been parsed!" % (packageName, language.short_name))
                return
        else:
            # Create the package in the databse
            package = Package(name=packageName)

        # Either a new package or the *.po is newer
        package.revisiondate = revisiondate
        package.save()

        valid_entries = [e for e in po if not e.obsolete]

        sentences = []

        try:
            for entry in valid_entries:
                sentence, created = Sentence.objects.get_or_create(msgid=entry.msgid)
                if entry.flags:
                    sentence.flags = ", ".join(entry.flags)

                if package not in sentence.packages.all():
                    sentence.packages.add(package)

                # Add translation
                translation, created = Translation.objects.get_or_create(msgstr=entry.msgstr, language=language)
                translation.translated = entry.translated()
                sentence.translations.add(translation)
                sentence.save()

                sentences.append(sentence)
        except Exception, e:
            logging.error("Failed to create sentences: %s" % str(e))
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
                sentence.length = len(sentence.words.all())


                sentence.save()

        except Exception, e:
            logging.error("Failed to create words: %s" % str(e))
            transaction.rollback()
        else:
            transaction.commit()
