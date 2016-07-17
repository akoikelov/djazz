import os
from django.core.management import BaseCommand, CommandError
import akoikelov
from akoikelov.djazz.management.commands.generators.admin_generator import AdminGenerator


class Command(BaseCommand):

    help = 'Generates admin class for given model'

    def add_arguments(self, parser):
        parser.add_argument('package', type=str)
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options):
        package = options['package']
        model_name = options['model_name']

        package_dir = os.getcwd() + '/' + package
        model_skeleton = open(os.path.join(akoikelov.djazz.__path__[0], 'conf', ) + '/model_class_template/admin.py-tpl').read()
        admin_file_resource = open(package_dir + '/admin.py', 'a')

        if not os.path.exists(package_dir):
            raise CommandError('Given package %s doesn\'t exist!' % package)

        generator = AdminGenerator(model_name, admin_file_resource, model_skeleton)
        generator.generate()

        self.stdout.write(self.style.SUCCESS('Admin for model %s successfully generated!' % model_name))