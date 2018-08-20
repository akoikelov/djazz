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
        admin_file_res = open(package_dir + '/admin.py', 'a')
        admin_file_res_read = open(package_dir + '/admin.py', 'r')

        if not os.path.exists(package_dir):
            raise CommandError('Given package %s doesn\'t exist!' % package)

        if 'from .models import *' not in ''.join(admin_file_res_read.readlines()):
            admin_file_res.write('\nfrom .models import *\n\n')

        admin_file_res_read.close()

        for m in models_names:
            if m + 'Admin' not in admin_names:
                generator = AdminGenerator(m, admin_file_res, admin_skeleton, package)
                generator.generate()
                generated_admin_models.append(m)

        admin_file_res.close()
        self.stdout.write(self.style.SUCCESS('Admin classes for models %s successfully generated!' % generated_admin_models))

    def execute(self, *args, **options):
        super(Command, self).execute(*args, **options)
        return 0