from typing import List

from django.urls import path, include, reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, URLPatternsTestCase

import formidable.urls
from administration.models import User
from formidable.models import Form, Section, Field, Validator
from tests.formidable.factories import (
    FormFactory,
    SectionFactory,
    FieldFactory,
    UserFactory,
    ValidatorFactory,
)


class ApplicationsApiTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include(formidable.urls.common_urls))]
    list_url = reverse("application-list")

    def setUp(self) -> None:
        self.form: Form = FormFactory.create()
        self.section: Section = SectionFactory.create(form=self.form)
        self.fields: List[Field] = FieldFactory.create_batch(3, section=self.section)
        self.validator: Validator = ValidatorFactory.create(field=self.fields[2])
        self.user: User = UserFactory.create()
        self.client.force_authenticate(user=self.user)

    def _assertFieldIsRequired(self, error):
        self.assertEqual(error.__len__(), 1)
        self.assertEqual(str(error[0]), "This field is required.")
        self.assertEqual(error[0].code, "required")

    def test_post_with_empty_body_returns_error(self):
        response = self.client.post(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self._assertFieldIsRequired(response.data.get("form"))
        self._assertFieldIsRequired(response.data.get("responses"))

    def test_post_with_no_form_returns_error(self):
        data = {
            "responses": [
                {
                    "value": "some value here that should work",
                    "field": self.fields[0].id,
                }
            ]
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self._assertFieldIsRequired(response.data.get("form"))

    def test_post_with_no_responses_returns_error(self):
        data = {"form": self.form.id}
        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self._assertFieldIsRequired(response.data.get("responses"))

    def test_authentication_is_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.list_url, {})
        detail: ErrorDetail = response.data.get("detail")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(detail), "Authentication credentials were not provided.")
        self.assertEqual(detail.code, "not_authenticated")

    def test_create_application_returns_201(self):
        data = {
            "form": self.form.id,
            "responses": [
                {"value": "random value with longer name", "field": self.fields[0].id},
                {"value": "anther value", "field": self.fields[1].id},
            ],
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
