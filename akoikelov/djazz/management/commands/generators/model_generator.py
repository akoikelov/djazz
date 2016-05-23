class ModelGenerator(object):

    def __init__(self, model_name):
        self.model_name = model_name
        self.templates = dict(
            field='%s = django.db.models.%s(%s)',
            max_length='max_length=%s',
            null='null=%s',
            verbose_name='verbose_name=\'%s\'',
            auto_now_add='auto_now_add=%s',
            auto_now='auto_now=%s'
        )
        self.fields = []

    def ask(self):
        name = raw_input('Field name?')

        if name == '':
            result = ''

            for i in range(0, len(self.fields)):
                if i == (len(self.fields) - 1):
                    result += self.fields[i]
                else:
                    result += self.fields[i] + '\n'

            return True, result

        type = raw_input('Field type?')
        verbose_name = self.templates['verbose_name'] % raw_input('Verbose name?')
        max_length = self.templates['max_length'] % raw_input('Max length?')
        null = self.templates['null'] % raw_input('Null?')

        field = self.templates['field'] % (name, type, '%s, %s, %s' % (max_length, null, verbose_name))
        self.fields.append(field)

        return False, ''
