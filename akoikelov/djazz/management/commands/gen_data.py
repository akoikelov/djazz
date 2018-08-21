import pyclbr

from django.core.management import BaseCommand
from django.db.models import Model

from akoikelov.djazz.management.commands.generators.data_generator import DataGenerator


class Command(BaseCommand):

    help = 'Generate initial data in database'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        package = options['app_name']
        models_module = package + '.models'
        models_names= list(a for a in pyclbr.readmodule(models_module))
        models = []

        m = __import__(models_module, fromlist=[package])

        for i in models_names:
            cl = getattr(m, i)

            if getattr(cl, '_gen_data', False) and issubclass(cl, Model):
                models.append(cl)

        generator = DataGenerator()
        generator.generate(models)