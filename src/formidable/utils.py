import datetime
from pprint import pprint


def get_upload_path(instance, filename: str) -> str:
    """
    Takes filename and creates new one with random string at the end
    :param instance: DO NOT delete this parameter, it's required for upload_to
    :param filename: raw file name from admin
    :return: new file name
    """
    if instance is None:
        filename, extension = filename.rsplit(".", 1)
        return f"{filename}_{str(datetime.datetime.now())[:19]}.{extension}"

    # noinspection PyProtectedMember
    model = instance.__class__._meta
    model_name = model.verbose_name_plural.replace(" ", "_")
    filename, extension = filename.rsplit(".", 1)
    return f"{model_name}/{filename}_{str(datetime.datetime.now())[:19]}.{extension}"


def log(obj):
    if isinstance(obj, list):
        [pprint(element.__dict__) for element in obj]
    pprint(obj.__dict__)


def get_filename(filename: str) -> str:
    return get_upload_path(None, filename)
