from typing import List

from django.urls import path, include, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase

import formidable.urls
from administration.models import User
from formidable.models import Form, Section, Field
from tests.formidable.factories import (
    FormFactory,
    SectionFactory,
    FieldFactory,
    UserFactory,
)


class ApplicationsApiTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include(formidable.urls.common_urls))]
    list_url = reverse("application-list")

    def setUp(self) -> None:
        self.form: Form = FormFactory.create()
        self.section: Section = SectionFactory.create(form=self.form)
        self.fields: List[Field] = FieldFactory.create_batch(4, section=self.section)
        self.fields[3].section = SectionFactory.create(form=self.form)
        self.fields[3].save()
        self.user: User = UserFactory.create()
        self.client.force_authenticate(user=self.user)

    def _assertFieldIsRequired(self, error):
        self.assertEqual(error.__len__(), 1)
        self.assertEqual(str(error[0]), "This field is required.")
        self.assertEqual(error[0].code, "required")
