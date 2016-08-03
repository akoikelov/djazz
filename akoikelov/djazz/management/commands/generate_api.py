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
        models_names = list(a.name for a in pyclbr.readmodule(package + '.models').values())

        package_dir = os.path.join(os.getcwd(), package)
        api_skeleton = open(os.path.join(akoikelov.djazz.__path__[0], 'conf', ) + '/tpl/api.py-tpl').read()
        api_file_resource = open(package_dir + '/api.py', 'a')
        urls = []
        urls_skeleton = "    url(r'^api/', include(%s().urls)),\n"
        url_data = ''

        with open(os.path.join(os.getcwd(), main_package_name) + '/urls.py', 'r') as w:
            data = w.readlines()

        for line in data:
            if not line.__contains__(']'):
                urls.append(line)
            else:
                line = line.replace(']', '')
                urls.append(line)

        if not os.path.exists(package_dir):
            raise CommandError('Given package %s doesn\'t exist!' % package)

        for m in models_names:
            generator = ApiGenerator(m, api_file_resource, api_skeleton)
            generator.generate()
            urls.append(urls_skeleton % m)

        urls.append(']\n')

        for i in urls:
            url_data += i

        urls_write_file_resource = open(os.path.join(os.getcwd(), main_package_name) + '/urls.py', 'w')
        urls_write_file_resource.write(url_data)
        urls_write_file_resource.close()
        api_file_resource.close()

        self.stdout.write(self.style.SUCCESS('Api classes for models %s successfully generated!' % models_names))