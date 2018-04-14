from distutils.dir_util import copy_tree
from random import random
from shutil import make_archive, copyfile, rmtree

import os

from django.core.management import CommandError, call_command


class BackupHelper(object):

    def __init__(self, media_root=None, media_archive_name='media'):
        self.media_root = media_root
        self.media_archive_name = media_archive_name

    def backup_and_compress(self, result_archive_name):
        file = 'db_dump_%s.json' % random()
        call_command('dumpdata', **{
            'output': file
        })

        return self._compress_all(db_file={
            'file': file,
            'delete': True
        }, result_archive_name=result_archive_name)

    def _compress_all(self, db_file, result_archive_name):
        if self.media_root is not None:
            if not os.path.exists(self.media_root):
                raise CommandError('MEDIA_ROOT path directory does not exist.')

        files = [db_file]

        if self.media_root:
            files.append({
                'folder': self.media_root,
                'delete': False
            })

        tmp_dir = 'backup_tmp_%s' % random()
        os.mkdir(tmp_dir)

        for f in files:
            if 'file' in f:
                copyfile(f['file'], '%s/%s' % (tmp_dir, f['file']))
            else:
                copy_tree(f['folder'], '%s/%s' % (tmp_dir, f['folder']))

            if f['delete']:
                if 'file' in f:
                    os.remove(f['file'])
                else:
                    rmtree(f['folder'])

        make_archive(result_archive_name, 'zip', tmp_dir)
        rmtree(tmp_dir)

        return '%s.zip' % result_archive_name

