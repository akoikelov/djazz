from django.conf import settings
from django.core.management import BaseCommand, CommandError

from akoikelov.djazz.management.commands.backup_helper.cloud import DropboxHelper
from akoikelov.djazz.management.commands.backup_helper.helper import *


class Command(BaseCommand):

    help = 'Save/load backup from/to cloud storage'

    BACKUP_HELPERS = {
        'django.db.backends.sqlite3': SQLiteBackupHelper,
        'django.db.backends.mysql': MySQLBackupHelper,
    }

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

        db_settings = settings.DATABASES['default']
        backup_helper = self.BACKUP_HELPERS[db_settings['ENGINE']](db_settings)