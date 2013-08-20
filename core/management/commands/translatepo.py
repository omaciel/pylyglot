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
from django.core.management.base import BaseCommand

from polib import pofile

from core.lib import translate

import logging
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--to-language', dest='to_language',
            help='Specifies the output language to translate to.'),
        make_option('--from-language', default='en', dest='from_language',
            help='Specifies the language to translate from.'),
    )

    args = '<po_file po_file ...>'
    help = 'Automatically translates a po file.'

    def handle(self, *args, **options):
        to_language = options.get('to_language',None)
        from_language = options.get('from_language','en')

        # po_file should come from SCRATCH_DIR
        logging.info("Scratch directory is %s." % settings.SCRATCH_DIR)

        for po_file in args:
            po = pofile(po_file, autodetect_encoding=True, encoding='utf-8', wrapwidth=80)
            entries = [e for e in po.untranslated_entries()]
            logging.info("%s untranslated entries." % len(entries))

            entries.extend([e for e in po.fuzzy_entries()])
            logging.info("%s fuzzy entries." % len(entries))

            for entry in entries:
                # TODO: first, check pylyglot's database for a match... try Google translate as fallback.
                t = translate(entry.msgid, to_language, from_language)
                entry.msgstr = t
                # Flag changes as fuzzy.
                if 'fuzzy' not in entry.flags:
                    entry.flags.insert(0, u'fuzzy')
                logging.info(t)
            po.save()
