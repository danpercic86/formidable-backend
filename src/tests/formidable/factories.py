import factory
from factory.django import DjangoModelFactory

from administration.models import User
from formidable.models import Form, Section, Field, Validator


class FormFactory(DjangoModelFactory):
    class Meta:
        model = Form

    name = factory.Faker("name")
    description = factory.Faker("text")


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    form = FormFactory.create()
    name = factory.Faker("name")
    description = factory.Faker("text")


class FieldFactory(DjangoModelFactory):
    class Meta:
        model = Field

    section = SectionFactory.create()
    name = factory.Faker("name")


class ValidatorFactory(DjangoModelFactory):
    class Meta:
        model = Validator

    field = FieldFactory.create()
    type = "minlength"
    constraint = 20


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = username
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True
