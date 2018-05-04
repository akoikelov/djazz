from django.db.models import Model, DateTimeField
from django.utils.text import slugify
from unidecode import unidecode


class AbstractModel(Model):

    class Meta:
        abstract = True

    created_at = DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    updated_at = DateTimeField(verbose_name='Обновлено', auto_now=True, null=True)

    def __unicode__(self):
        pass

    def __str__(self):
        return self.__unicode__()


class ModelWithSlugMixin(AbstractModel):

    slugifying_field_name = 'name'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(getattr(self, self.slugifying_field_name)))
        super(ModelWithSlugMixin, self).save(*args, **kwargs)