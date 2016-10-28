import os
import pyclbr
from django.core.management import BaseCommand, CommandError
import akoikelov
from akoikelov.djazz.management.commands.generators.api_generator import ApiGenerator


class Command(BaseCommand):

    help = 'Generates api resource class for app models'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('main_app_name', type=str)

    def handle(self, *args, **options):
        package = options['app_name']
        main_package_name = options['main_app_name']

        package_dir = os.path.join(os.getcwd(), package)
        if not os.path.exists(package_dir):
            raise CommandError('Given package %s doesn\'t exist!' % package)

        api_skeleton = open(os.path.join(akoikelov.djazz.__path__[0], 'conf', ) + '/tpl/api.py-tpl').read()
        api_file_resource = open(package_dir + '/api.py', 'a')
        urls = ''
        urls_skeleton = "\nurlpatterns.append(url(r'^api/', include(%sResource().urls)))"

        models_names = list(a.name for a in pyclbr.readmodule(package + '.models').values())
        api_names = list(a.name for a in pyclbr.readmodule(package + '.api').values())
        generated_api_models = []
        api_resource_classes = []

        for m in models_names:
            if m + 'Resource' not in api_names:
                generator = ApiGenerator(m, api_file_resource, api_skeleton, package + '.models')
                generator.generate()
                urls += urls_skeleton % m
                generated_api_models.append(m)
                api_resource_classes.append(m + 'Resource')

        api_resource_import = '\n\nfrom %s.api import %s' % (package, ', '.join(c for c in api_resource_classes))
        urls_write_file_resource = open(os.path.join(os.getcwd(), main_package_name) + '/urls.py', 'a')

        if api_resource_classes.__len__() > 0:
            urls_write_file_resource.write('%s\n' % api_resource_import)

        urls_write_file_resource.write('%s' % urls)
        urls_write_file_resource.close()
        api_file_resource.close()

        self.stdout.write(self.style.SUCCESS('Api classes for models %s successfully generated!' % generated_api_models))

    def execute(self, *args, **options):
        super(Command, self).execute(*args, **options)
        return 0
