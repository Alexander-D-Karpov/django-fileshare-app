from typing import IO

from django.http import HttpResponse

from file.models import File, Group, GroupFile
from user.models import Person


def file_upload(
        files: list[IO],
        user: Person,
        name: str = "",
        description: str = "",
        group_slug: str = "",
) -> File:
    """creates file instance or raises exception"""
    i = 0
    for f in files:
        if user.left_file_upload < f.size:
            raise Exception

        f_name = (
            name + ("-" + str(i) if i != 0 else "") if name else (f.name.split(".")[0])
        )
        file = File(
            name=f_name,
            description=description,
            user=user,
            file=f,
        )
        file.gen_file()
        if group_slug:
            if group := Group.objects.filter(slug=group_slug):
                GroupFile.objects.create(group=group[0], file=file)
            else:
                group = Group.objects.create(name=group_slug, private=True)
                GroupFile.objects.create(group=group, file=file)

        i += 1


"""
def f_file_upload(files: list[IO], user: Person, name: str = "", description: str = "", group_name: str = "") -> None:
    [(fl := File(name=name if name else (files[i].name.split(".")[0] + ("-" + str(i) if i != 0 else "")), description=description, user=user, file=files[i]), fl.gen_file(), fl.save(), GroupFile.objects.create(group=Group.objects.get(name=group_name) if Group.objects.filter(name=group_name).exists() else GroupFile.objects.create(group=Group.objects.create(name=group_name, private=True))) if group_name else "") for i in range(len(files))]
"""
