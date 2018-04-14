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
        parser.add_argument('--load', action='store_true', dest='load', help='load backup')

    def handle(self, *args, **options):
        if not hasattr(settings, 'DROPBOX_ACCESS_TOKEN'):
            raise CommandError('DROPBOX_ACCESS_TOKEN is not set in settings')

        action = None

        if options['save']:
            action = 'save'
        elif options['load']:
            action = 'load'

        if action is None:
            raise CommandError('Please provide right action: --save or --load')

        dropbox = DropboxHelper(access_token=settings.DROPBOX_ACCESS_TOKEN)

        if not hasattr(settings, 'DATABASES'):
            raise CommandError('Please provide database settings')

        include_media = options['include-media']

        if include_media and not hasattr(settings, 'MEDIA_ROOT'):
            raise CommandError('MEDIA_ROOT is not provided')

        if action == 'save':
            backup_helper = BackupHelper(media_root=settings.MEDIA_ROOT if include_media else None)

            activate(settings.TIME_ZONE)

            result_archive_name = 'backup-%s' % datetime.now().strftime('%Y-%m-%d_%H:%M')
            compressed_file = backup_helper.backup_and_compress(result_archive_name)

            dropbox.upload(compressed_file)
        else:
            raise CommandError('Action --load not implemented yet.')