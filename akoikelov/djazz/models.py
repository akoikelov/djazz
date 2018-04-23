from django.db.models import Model, DateTimeField


class AbstractModel(Model):

    class Meta:
        abstract = True

    created_at = DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    updated_at = DateTimeField(verbose_name='Обновлено', auto_now=True, null=True)

    def __unicode__(self):
        pass

    def __str__(self):
        return self.__unicode__()