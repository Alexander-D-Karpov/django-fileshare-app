import ffmpeg
from django.core.files.images import get_image_dimensions
from django.http import Http404

from file.models import File
from user.models import Person


def get_file(slug: str, user: Person = None) -> dict:
    data = {}
    if file := File.objects.filter(slug=slug):
        file = file[0]
        data["file"] = file
        if file.file.size < 1048576 and ("text" in file.type or "application" in file.type):
            content = open(file.file.path, 'rb').read().decode('ISO-8859-1')
        else:
            content = "can't load the file"
        data["content"] = content
    else:
        raise Http404
    if user:
        data["is_saved"] = File.objects.filter(slug=slug, user=user).exists() or File.objects.filter(
            slug=slug + "-" + user.username, user=user).exists()

    if "image" in file.type:
        data["width"], data["height"] = get_image_dimensions(file.file.file)
    elif "video" in file.type:
        dat = ffmpeg.probe(file.file.path)["streams"]
        data["width"], data["height"] = dat[0]["width"], dat[0]["height"]

    return data
