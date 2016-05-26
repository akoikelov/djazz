from django.template import Template, Context


class ModelGenerator(object):

    FIELDS_TYPE_AUTOCOMPLETE = [
        'char', 'text', 'date', 'datetime', 'decimal',
        'email', 'float', 'int', 'url', 'bool', 'nullbool', 'fkey'
    ]

    def __init__(self, model_name, model_skeleton, models_file_resource, command_instance):
        self.model_name = model_name
        self.model_skeleton = model_skeleton
        self.models_file_resource = models_file_resource
        self.templates = dict(
            field='%s = models.%s(%s)',
            max_length='max_length=%s',
            null='null=%s',
            blank='blank=%s',
            unique='unique=%',
            verbose_name='verbose_name=\'%s\'',
            auto_now_add='auto_now_add=%s',
            auto_now='auto_now=%s',
            fkey_model='%s',
            on_del='on_delete=%s',
            to='to=%s'
        )
        self.fieldTypePairs = dict(
            char='CharField', text='TextField', date='DateField', datetime='DateTimeField',
            decimal='DecimalField', email='EmailField', float='FloatField', int='IntegerField',
            url='URLField', bool='BooleanField', nullbool='NullBooleanField', fkey='ForeignKey'
        )
        self.fields = []
        self.command_instance = command_instance

    def ask(self):
        field_name = raw_input('Field name? ')

        if field_name == '':
            return True

        field_type = self.fieldTypePairs[raw_input('Field type? ')]
        verbose_name = self.templates['verbose_name'] % field_name
        max_length = self.templates['max_length'] % raw_input('Max length? ')
        nullable = raw_input('Null?[False] ')

        if nullable == '':
            nullable = self.templates['null'] % 'False'
        else:
            nullable = self.templates['null'] % nullable

        self.command_instance.stdout.write('\n')
        add_more_fields = raw_input('Add more fields?[yes]')

        field = self.templates['field'] % (field_name, field_type, '%s, %s, %s' % (max_length, nullable, verbose_name))
        self.fields.append(field)

        if add_more_fields == 'no':
            return True

        return False

    def generate(self):
        template = Template(self.model_skeleton)
        context = Context(dict(model_name=self.model_name, fields=self.fields))

        generated = template.render(context)

        self.models_file_resource.write(generated)
        self.models_file_resource.close()
