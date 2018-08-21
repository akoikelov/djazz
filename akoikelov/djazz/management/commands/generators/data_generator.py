
from django.db.models.fields import *


class DataGenerator(object):

    def generate(self, models):
        for m in models:
            fields = [i for i in m._meta.fields]