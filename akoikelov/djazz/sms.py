import os

import requests
from django.template import Template, Context

import akoikelov
from .exceptions import NikitaBadResponseException


class NikitaSmsHelper(object):

    template_name = 'templates/nikita/sms.xml'
    endpoint = 'http://smspro.nikita.kg/api/message'

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_sms(self, id, sender, text, phones, test=1):
        context = {
            'login': self.login,
            'password': self.password,
            'id': id,
            'sender': sender,
            'text': text,
            'phones': phones,
            'test': test
        }

        rendered = self.render(context)

        response = requests.post(self.endpoint, data=rendered.encode('utf-8'), headers={
            'Content-Type': 'application/xml'
        })

        if response.status_code == 200:
            return response.content.decode('utf-8')

        raise NikitaBadResponseException()

    def render(self, context):
        content = open(os.path.join(akoikelov.djazz.__path__[0], self.template_name)).read()
        tpl = Template(content)

        return tpl.render(Context(context))