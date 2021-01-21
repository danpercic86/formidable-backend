from typing import AnyStr

from django.contrib.admin import ModelAdmin
from django.db.models import Model, SlugField

from formidable.model_fields import CREATED, MODIFIED, SLUG, NAME


#               MODELS
class SlugableModel(Model):
    slug = SlugField(unique=True, db_index=True)

    class Meta:
        abstract = True


class BaseModel(Model):
    class Meta:
        abstract = True

    def __str__(self):
        if name := getattr(self, NAME, None):
            return name
        if title := getattr(self, "title", None):
            return title
        if slug := getattr(self, SLUG, None):
            return slug
        return self.__class__.__name__ + " " + str(self.id)

    def get_change_url(self) -> AnyStr:
        from django.urls import reverse_lazy

        return reverse_lazy(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_change",
            args=[str(self.id)],
        )

    @property
    def href(self):
        """
        Use this property in admin dashboard to show this object's name as html anchor
        that redirects to object's edit page
        @return:
        """
        from django.utils.html import format_html

        return format_html(f"<a href='{self.get_change_url()}'>{self}</a>")


#              ADMIN
class BaseModelAdmin(ModelAdmin):
    list_filter = (CREATED, MODIFIED)
    readonly_fields = (CREATED, MODIFIED)


class SlugableModelAdmin(ModelAdmin):
    prepopulated_fields = {SLUG: (NAME,)}
