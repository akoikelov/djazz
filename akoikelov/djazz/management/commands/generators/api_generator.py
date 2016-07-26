from django.template import Context, Template


class ApiGenerator(object):

    def __init__(self, model_name, api_file_resource, api_skeleton):
        self.model_name = model_name
        self.api_file_resource = api_file_resource
        self.api_skeleton = api_skeleton

    def generate(self):
        template = Template(self.api_skeleton)
        context = Context(dict(model_name=self.model_name))

        result = template.render(context)
        self.api_file_resource.write(result)