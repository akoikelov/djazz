import zipfile
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.timezone import activate

from akoikelov.djazz.management.commands.backup_helper.cloud import DropboxHelper
from akoikelov.djazz.management.commands.backup_helper.helper import *


class Command(BaseCommand):

    help = 'Save/load backup from/to cloud storage'

    def add_arguments(self, parser):
        parser.add_argument('--include-media', action='store_true', dest='include-media', help='Include media folder '
                                                                                               'to backup')
        parser.add_argument('--save', action='store_true', dest='save', help='Save backup')
        parser.add_argument('--load', action='store_true', dest='load', help='Load backup')
        parser.add_argument('--replace', action='store_true', dest='replace', help='Delete old backups and replace '
                                                                                   'them with a new')

    def handle(self, *args, **options):
        if not hasattr(settings, 'DROPBOX_ACCESS_TOKEN'):
            raise CommandError('DROPBOX_ACCESS_TOKEN is not set in settings')

        action = None
        replace = options['replace']

        if options['save']:
            action = 'save'
        elif options['load']:
            action = 'load'

        if action is None:
            raise CommandError('Please provide right action: --save or --load')

        if not hasattr(settings, 'DATABASES'):
            raise CommandError('Please provide database settings')

        include_media = options['include-media']
        dropbox = DropboxHelper(access_token=settings.DROPBOX_ACCESS_TOKEN)
        backup_helper = BackupHelper(media_root=settings.MEDIA_ROOT if include_media else None)

        if include_media and not hasattr(settings, 'MEDIA_ROOT'):
            raise CommandError('MEDIA_ROOT is not provided')

        if action == 'save':
            self._save(backup_helper, dropbox, replace)
        else:
            self._load(backup_helper, dropbox)

    def _save(self, backup_helper, dropbox, replace):
        activate(settings.TIME_ZONE)
        result_archive_name = 'backup-%s' % datetime.now().strftime('%Y-%m-%d_%H:%M')
        compressed_file = backup_helper.backup_and_compress(result_archive_name)

        try:
            if replace:
                dropbox.delete_all_files()

            dropbox.upload(compressed_file)
        except:
            pass

        os.remove(compressed_file)

    def _load(self, backup_helper, dropbox):
        working_dir = os.getcwd()
        path_to_file, hash = dropbox.download_last_backup(working_dir)

        with zipfile.ZipFile(path_to_file, 'r') as zip_file:
            zip_file.extractall('%s/%s' % (working_dir, hash))