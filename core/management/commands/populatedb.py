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
from django.core.management.base import AppCommand
from django.core.management.base import BaseCommand, CommandError

from polib import pofile

from pylyglot.core.models import Job, Language, Package
from pylyglot.core.lib import populate_db

import tempfile
from urllib import urlopen

import logging

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Check if exists any Job and create them if necessary
        for language in Language.objects.all():
            for package in Package.objects.all():
                (job, created) = Job.objects.get_or_create(language=language, package=package)
                if created:
                    job.save()

        active_job = Job.objects.filter(active = True)
        if active_job:
            logging.info("There's a job being run right now for %s - %s later" % (active_job[0].package.name, active_job[0].language.short_name))
            logging.info("Will try again later!")
            return

        job = Job.objects.order_by('update_on')[0]
        logging.info("Running task for %s - %s" % (job.package.name, job.language.short_name))
        logging.info("Setting job to 'active'.")
        job.active = True
        job.save()

        try:
            url = "%s.%s.po" % (job.package.src_url, job.language.short_name)
            logging.info("Fetching file from %s" % url)
            remote_file = urlopen(url)

            (fd, filename) = tempfile.mkstemp(job.package.name)
            f = os.fdopen(fd, "w")

            for line in remote_file.readlines():
                f.write(line)
            f.close()
            logging.info("File has been downloaded.")

            try:
                po = pofile(filename, autodetect_encoding=True, encoding='utf-8')
                populate_db(po, job.language, job.package)
            except Exception, e:
                logging.error("Failed to open po file %s for %s" % (job.package.name, job.language.short_name))
                logging.error("Error: %s" % str(e))


        except Exception, e:
            logging.error("Failed to download the file located on %s" % url)
            logging.error("Error: %s" % str(e))
        finally:
            # Extract what we need from the "old" job
            package = job.package
            language = job.language
            # Delete this job...
            logging.info(job.update_on)
            job.delete()
            logging.info("Job has been deleted.")
            # ... and create a new one, put it at the end of queue.
            (job, created) = Job.objects.get_or_create(language=language, package=package)
            job.save()
            logging.info("New job has been created.")
            logging.info(job.update_on)
