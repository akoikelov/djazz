import shutil
import subprocess
from distutils.dir_util import copy_tree
from random import random
from shutil import make_archive, copyfile, rmtree

from django.conf import settings
from django.core.management import CommandError

import os


class BackupHelper(object):

    def __init__(self, media_root=None, media_archive_name='media'):
        self.media_root = media_root
        self.media_archive_name = media_archive_name

    def backup_and_compress(self, result_archive_name):
        dumper = self.Dumper()
        files = dumper.create_dumps(db_config=settings.DATABASES)

        return self._compress_all(db_files=[{
            'file': f,
            'delete': True
        } for f in files], result_archive_name=result_archive_name)

    def _compress_all(self, db_files, result_archive_name):
        if self.media_root is not None:
            if not os.path.exists(self.media_root):
                raise CommandError('MEDIA_ROOT path directory does not exist.')

        files = db_files

        if self.media_root:
            files.append({
                'folder': self.media_root,
                'delete': False
            })

        tmp_dir = 'backup_tmp_%s' % random()
        os.mkdir(tmp_dir)

        curr_dir = os.getcwd()

        for f in files:
            if 'file' in f:
                copyfile(f['file'], '%s/%s' % (tmp_dir, f['file']))
            else:
                os.chdir(os.path.join(f['folder'], '../'))
                media_folder_name = os.path.basename(os.path.normpath(f['folder']))

                copy_tree(f['folder'], '%s/%s' % (tmp_dir, media_folder_name))
                os.chdir(curr_dir)

            if f['delete']:
                if 'file' in f:
                    os.remove(f['file'])
                else:
                    rmtree(f['folder'])

        tmp_dir_path = os.path.join(os.getcwd(), tmp_dir)

        make_archive(result_archive_name, 'zip', tmp_dir_path)
        rmtree(tmp_dir)

        filename = '%s.zip' % result_archive_name

        return filename, os.path.join(os.getcwd(), filename)

    def load_backup(self, backup_folder_path):
        pass

    class Dumper(object):

        def create_dumps(self, db_config):
            filename_tpl = '{id}_dump_{db}'
            files = []

            for k in db_config:
                config = db_config[k]
                filename = filename_tpl.format(id=random(), db=k)

                if 'sqlite3' in config['ENGINE']:
                    self._dump_sqlite(config, filename)
                elif 'mysql' in config['ENGINE']:
                    self._dump_mysql(config, filename)
                elif 'postgresql' in config['ENGINE']:
                    self._dump_pg(config, filename)

                files.append(filename)

            return files

        def _dump_sqlite(self, config, filename):
            shutil.copy(config['NAME'], filename)

        def _dump_mysql(self, config, filename):
            command = "mysqldump --user='%s' --password='%s' -h %s -e --opt -c %s > %s" % (
                config['USER'], config['PASSWORD'], config['HOST'], config['NAME'], filename)

            p = subprocess.Popen(command, shell=True)
            p.wait()

        def _dump_pg(self, config, filename):
            command = 'export PGPASSWORD="%s" && pg_dump -h %s -U %s %s > %s' % (
                config['PASSWORD'],
                config['HOST'], config['USER'], config['NAME'], filename
            )

            p = subprocess.Popen(command, shell=True)
            p.wait()
