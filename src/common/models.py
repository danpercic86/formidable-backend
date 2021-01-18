from typing import AnyStr

from django.db.models import Model, SlugField


class SlugableModel(Model):
    slug = SlugField(unique=True, db_index=True)

    class Meta:
        abstract = True


class BaseModel(Model):
    class Meta:
        abstract = True

    def get_change_url(self) -> AnyStr:
        from django.urls import reverse_lazy

        return reverse_lazy(
            f'admin:{self._meta.app_label}_{self._meta.model_name}_change',
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
