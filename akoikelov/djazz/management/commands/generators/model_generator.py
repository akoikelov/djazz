from django.template import Template, Context


class ModelGenerator(object):

    def __init__(self, model_name, model_skeleton, models_file_resource):
        self.model_name = model_name
        self.model_skeleton = model_skeleton
        self.models_file_resource = models_file_resource
        self.templates = dict(
            field='%s = models.%s(%s)',
            max_length='max_length=%s',
            null='null=%s',
            verbose_name='verbose_name=\'%s\'',
            auto_now_add='auto_now_add=%s',
            auto_now='auto_now=%s'
        )
        self.fields = []

    def ask(self):
        field_name = raw_input('Field name?')

        if field_name == '':
            return True

        field_type = raw_input('Field type?')
        verbose_name = self.templates['verbose_name'] % raw_input('Verbose name?')
        max_length = self.templates['max_length'] % raw_input('Max length?')
        nullable = self.templates['null'] % raw_input('Null?')

        field = self.templates['field'] % (field_name, field_type, '%s, %s, %s' % (max_length, nullable, verbose_name))
        self.fields.append(field)

        return False

    def generate(self):
        template = Template(self.model_skeleton)
        context = Context(dict(model_name=self.model_name, fields=self.fields))

        generated = template.render(context)

        self.models_file_resource.write(generated)
        self.models_file_resource.close()