from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--include-media', action='store_true', dest='include-media', help='Include media folder to backup')

    def handle(self, *args, **options):
        pass