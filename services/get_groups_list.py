from file.models import Group
from user.models import Person


def get_group_list(user: Person = None):
    if user and user.is_superuser:
        return Group.objects.all()
    else:
        return Group.objects.filter(private=False)