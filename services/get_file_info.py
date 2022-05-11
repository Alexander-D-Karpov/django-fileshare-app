import time
from typing import IO

import magic
from django.utils.text import slugify

from file.models import File
from user.models import Person


def file_upload(*, name: str, description: str, username: str, file: IO) -> File:
    slug = slugify(name + str(time.time()))
    File.objects.create(
        name=name,
        description=description,
        user=Person.objects.get(username=username),
        slug=slug,
        file=file,
    ).save()
    file = File.objects.get(slug=slug)
    file.type = magic.from_file(file.file.path)
    file.save()
    return file
