import os
from django.core.management import call_command
from django.test import TestCase


class TestGenerateApiCommand(TestCase):

    SUCCESS_CODE = 0

    def setUp(self):
        if not os.path.exists(os.getcwd() + '/dummytestappforgenerateapi'):
            call_command('startapp', 'dummytestappforgenerateapi')
            call_command('startapp', 'dummymaintestappforgenerateapi')

    def test_generate_admin_class(self):
        result = call_command('generate_api', 'dummytestappforgenerateapi', 'dummymaintestappforgenerateapi')
        self.assertEqual(result, self.SUCCESS_CODE)