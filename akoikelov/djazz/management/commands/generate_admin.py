import os
import pyclbr
from django.core.management import BaseCommand, CommandError
import akoikelov
from akoikelov.djazz.management.commands.generators.admin_generator import AdminGenerator


class Command(BaseCommand):

    help = 'Generates admin class for given model'

    def add_arguments(self, parser):
        parser.add_argument('package', type=str)

    def handle(self, *args, **options):
        package = options['package']
        models_names = list(a.name for a in pyclbr.readmodule(package + '.models').values())

        package_dir = os.path.join(os.getcwd(), package)
        model_skeleton = open(os.path.join(akoikelov.djazz.__path__[0], 'conf', ) + '/model_class_template/admin.py-tpl').read()
        admin_file_resource = open(package_dir + '/admin.py', 'a')

        if not os.path.exists(package_dir):
            raise CommandError('Given package %s doesn\'t exist!' % package)

        for m in models_names:
            generator = AdminGenerator(m, admin_file_resource, model_skeleton, package)
            generator.generate()

        admin_file_resource.close()
        self.stdout.write(self.style.SUCCESS('Admin classes for models %s successfully generated!' % models_names))