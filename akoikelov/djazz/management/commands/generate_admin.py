import os
import pyclbr
from django.core.management import BaseCommand, CommandError
import akoikelov
from akoikelov.djazz.management.commands.generators.admin_generator import AdminGenerator


class Command(BaseCommand):

    help = 'Generates admin classes for existing models inside app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        package = options['app_name']
        models_names = list(a.name for a in pyclbr.readmodule(package + '.models').values())
        admin_names = list(a.name for a in pyclbr.readmodule(package + '.admin').values())
        generated_admin_models = []

        package_dir = os.path.join(os.getcwd(), package)
        admin_skeleton = open(os.path.join(akoikelov.djazz.__path__[0], 'conf', ) + '/tpl/admin.py-tpl').read()
        admin_file_resource = open(package_dir + '/admin.py', 'a')

        if not os.path.exists(package_dir):
            raise CommandError('Given package %s doesn\'t exist!' % package)

        for m in models_names:
            if m + 'Admin' not in admin_names:
                generator = AdminGenerator(m, admin_file_resource, admin_skeleton, package)
                generator.generate()
                generated_admin_models.append(m)

        admin_file_resource.close()
        self.stdout.write(self.style.SUCCESS('Admin classes for models %s successfully generated!' % generated_admin_models))
