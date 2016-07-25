from pydoc import locate
from django.template import Template, Context


class AdminGenerator(object):

    def __init__(self, model_name, admin_file_resource, model_skeleton, package):
        self.model_name = model_name
        self.admin_name = model_name + 'Admin'
        self.admin_file_resource = admin_file_resource
        self.model_skeleton = model_skeleton
        self.package = package + '.models.'

    def generate(self):
        obj = locate(self.package + self.model_name)()
        fields = list(a for a in obj.__dict__ if not a.startswith('_'))
        fields.reverse()

        template = Template(self.model_skeleton)
        context = Context(dict(model_name=self.model_name, admin_name=self.admin_name, fields=fields))

        generated = template.render(context)
        self.admin_file_resource.write(generated)