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

        model_skeleton = open(os.path.dirname(__file__) + '/skeleton/model.py.skeleton').read()
        models_file_resource = open(package_dir + '/models.py', 'a')
        generator = ModelGenerator(model_name, model_skeleton, models_file_resource)
        finished = False

        while not finished:
            finished = generator.ask()
            self.stdout.write('\n')

            if finished:
                break

        generator.generate()
        self.stdout.write('all done!')
