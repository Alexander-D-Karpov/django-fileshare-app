from django.http import Http404

from file.models import File, Group, GroupFile
from user.models import Person


def get_file_list(user: Person = None, group_slug: str = "") -> list[File]:
    if group_slug:
        if group := Group.objects.filter(slug=group_slug):
            return [x.file for x in GroupFile.objects.filter(group=group[0])]
        else:
            raise Http404
    else:
        return sorted(
                File.objects.filter(user=user),
                key=lambda x: x.id,
                reverse=True,
            )
