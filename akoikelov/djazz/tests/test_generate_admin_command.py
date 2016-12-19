import os
from django.core.management import call_command
from django.test import TestCase


class TestGenerateAdminCommand(TestCase):

    SUCCESS_CODE = 0

    def setUp(self):
        if not os.path.exists(os.getcwd() + '/dummytestappforgenerateadmin'):
            call_command('startapp', 'dummytestappforgenerateadmin')

    def test_generate_admin_class(self):
        result = call_command('generate_admin', 'dummytestappforgenerateadmin')
        self.assertEqual(result, self.SUCCESS_CODE)