import os
from akoikelov.djazz.management.commands.generators.model_generator import ModelGenerator
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('package', type=str)
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options):
        package = options['package']
        model_name = options['model_name']

        package_dir = settings.BASE_DIR + '/' + package

        if not os.path.exists(package_dir):
            self.stderr.write('Given package %s doesn\'t exist!' % package)
            return

        generator = ModelGenerator(model_name)
        finished = False
        fields = None

        while not finished:
            finished, fields = generator.ask()
            self.stdout.write('\n')

            if finished:
                break

        module_path = os.path.dirname(__file__)
        model_skeleton = open(module_path + '/skeleton/model.py.skeleton').read()
        models_file = open(package_dir + '/models.py', 'a')

        models_file.write(model_skeleton % (model_name, fields))
        models_file.close()

        self.stdout.write('all done!')
