from typing import List

from django.urls import path, include, reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, URLPatternsTestCase

import formidable.urls
from administration.models import User
from formidable.constants import Errors, Codes
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

    def test_create_application_successful(self):
        self.fields[0].is_required = True
        self.fields[0].save()
        self.fields[1].is_required = True
        self.fields[1].save()
        data = {
            "form": self.form.id,
            "responses": [
                {"value": "random value with longer name", "field": self.fields[0].id},
                {"value": "some thing here", "field": self.fields[1].id},
                {"value": "anther value", "field": self.fields[2].id},
            ],
        }

        # self.validator: Validator = ValidatorFactory.create(field=self.fields[0])

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_application_returns_error_when_field_from_different_section(self):
        data = {
            "form": self.form.id,
            "responses": [
                {"value": "random value with longer name", "field": self.fields[3].id},
                {"value": "some thing here", "field": self.fields[1].id},
                {"value": "anther value", "field": self.fields[2].id},
            ],
        }

        response = self.client.post(self.list_url, data)
        detail: List[ErrorDetail] = response.data[Codes.NOT_SAME_SECTION]
        self.assertEqual(len(detail), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(detail[0], Errors.NotSameSection)

    def test_create_application_returns_error_when_missing_required_fields(self):
        self.fields[0].is_required = True
        self.fields[0].save()
        self.fields[1].is_required = True
        self.fields[1].save()
        data = {
            "form": self.form.id,
            "responses": [
                {"value": "random value with longer name", "field": self.fields[0].id},
                {"value": "anther value", "field": self.fields[2].id},
            ],
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertGreaterEqual(len(response.data.values()), 1)

        for detail in response.data.values():  # type: List[ErrorDetail]
            self.assertEqual(len(detail), 1)
            self.assertEqual(detail[0], Errors.RequiredField)
