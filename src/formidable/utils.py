import datetime
from pprint import pprint


def get_upload_path(instance, file_name: str) -> str:
    """
    Takes filename and creates new one with random string at the end
    :param instance: DO NOT delete this parameter, it's required for upload_to
    :param file_name: raw file name from admin
    :return: new file name
    """
    if instance is None:
        file_name, extension = file_name.rsplit(".", 1)
        return f"{file_name}_{str(datetime.datetime.now())[:19]}.{extension}"

    # noinspection PyProtectedMember
    model = instance.__class__._meta
    model_name = model.verbose_name_plural.replace(" ", "_")
    file_name, extension = file_name.rsplit(".", 1)
    return f"{model_name}/{file_name}_{str(datetime.datetime.now())[:19]}.{extension}"


def log(obj):
    if isinstance(obj, list):
        [pprint(element.__dict__) for element in obj]
    pprint(obj.__dict__)
