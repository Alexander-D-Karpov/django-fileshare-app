from django.http import Http404

from file.models import File
from user.models import Person


def del_file(slug: str, user: Person) -> None:
    if file := File.objects.filter(slug=slug, user=user):
        file = file[0]
    else:
        raise Http404

    file.delete()
