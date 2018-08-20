from pydoc import locate
from django.template import Template, Context


class AdminGenerator(object):

    def __init__(self, model_name, admin_file_resource, admin_skeleton, package):
        self.model_name = model_name
        self.admin_name = model_name + 'Admin'
        self.admin_file_resource = admin_file_resource
        self.model_skeleton = admin_skeleton
        self.package = package + '.models.'
        self.models = package + '.models'

    def generate(self):
        obj = locate(self.package + self.model_name)()
        fields = list(f.name for f in obj._meta.fields)
        fields.reverse()

        template = Template(self.model_skeleton)
        context = Context(dict(model_name=self.model_name, admin_name=self.admin_name, fields=fields, models=self.models))

        generated = template.render(context)
        self.admin_file_resource.write(generated)