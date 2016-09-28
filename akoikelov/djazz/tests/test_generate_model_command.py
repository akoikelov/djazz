import os
from StringIO import StringIO
from django.core.management import call_command
from django.test import TestCase
from mock import mock


class RawInputMock(object):

    def mock_raw_input(self, question, field_name, field_type):
        if question.__contains__('Field name?'):
            return field_name
        elif question.__contains__('Field type?'):
            return field_type
        elif question.__contains__('Max length?'):
            return '1000'
        elif question.__contains__('Unique?[False]') or question.__contains__('Null?[False]'):
            return ''
        elif question.__contains__('Add more fields?[yes]'):
            return 'no'
        elif question.__contains__('Related model name?'):
            return ''
        elif question.__contains__('On delete?[models.CASCADE]'):
            return ''
        elif question.__contains__('ManyToMany model name?'):
            return 'TestManyToMany2'
        elif question.__contains__('Through model??'):
            return 'TestThroughModel'

    def primitive_field_mock(self, question):
        return self.mock_raw_input(question=question, field_type='char', field_name='title')

    def foreignkey_field_mock(self, question):
        return self.mock_raw_input(question=question, field_type='fkey', field_name='testForeignKey')

    def manytomany_field_mock(self, question):
        return self.mock_raw_input(question=question, field_type='mtm', field_name='testManyToMany')


class TestGenerateModelCommand(TestCase):

    SUCCESS_CODE = 0

    def setUp(self):
        self.mock = RawInputMock()

        if not os.path.exists(os.getcwd() + '/dummytestappforgeneratemodel'):
            call_command('startapp', 'dummytestappforgeneratemodel')

    def test_generate_primitive_field(self):
        with mock.patch('__builtin__.raw_input', self.mock.primitive_field_mock):
            out = StringIO()
            result = call_command('generate_model', 'dummytestappforgeneratemodel', 'TestPrimitive', stdout=out)
            self.assertEqual(result, self.SUCCESS_CODE)
            self.assertEqual(out.getvalue().replace('\n', ''), 'Model TestPrimitive successfully generated!')

    def test_generate_foreignkey_field(self):
        with mock.patch('__builtin__.raw_input', self.mock.foreignkey_field_mock):
            out = StringIO()
            result = call_command('generate_model', 'dummytestappforgeneratemodel', 'TestForeignKey', stdout=out)
            self.assertEqual(result, self.SUCCESS_CODE)
            self.assertEqual(out.getvalue().replace('\n', ''), 'Model TestForeignKey successfully generated!')

    def test_generate_manytomany_field(self):
        with mock.patch('__builtin__.raw_input', self.mock.manytomany_field_mock):
            out = StringIO()
            result = call_command('generate_model', 'dummytestappforgeneratemodel', 'TestManyToMany', stdout=out)
            self.assertEqual(result, self.SUCCESS_CODE)
            self.assertEqual(out.getvalue().replace('\n', ''), 'Model TestManyToMany successfully generated!')