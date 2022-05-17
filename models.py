import os
import secrets
import string

import magic
from django.conf import settings
from django.db import models
from django.urls import reverse

from file.services.get_svg import get_svg
from user.models import Person as User


# Create your models here.


class File(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/files/", blank=False)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=False, unique=True)
    type = models.CharField(max_length=50, blank=False, default="none")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("file_view", kwargs={"slug": self.slug})

    def gen_file(self, *args, **kwargs):
        alphabet = string.ascii_letters + string.digits
        self.slug = "".join(secrets.choice(alphabet) for _ in range(10))
        extension = os.path.splitext(self.file.name)[1]
        self.file.name = self.slug + extension
        super(File, self).save(*args, **kwargs)
        self.type = magic.from_file(self.file.path, mime=True)
        super(File, self).save(*args, **kwargs)
        self.user.left_file_upload -= self.file.size
        self.user.save(update_fields=["left_file_upload"])

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            self.user.left_file_upload += self.file.size
            os.remove(self.file.path)
            self.user.save(update_fields=["left_file_upload"])
        super(File, self).delete()

    def delete_safe(self):
        super(File, self).delete()

    def svg(self):
        return get_svg(self.type)


class Group(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(blank=False, unique=True)
    private = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.private:
            self.slug = "".join(secrets.choice(string.ascii_letters) for _ in range(10))
        else:
            self.slug = self.name
        super(Group, self).save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Group"

    def get_absolute_url(self):
        return reverse("file_group", kwargs={"slug": self.slug})


class GroupFile(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        db_table = "GroupFile"

    def __str__(self):
        return self.group.name + " - " + self.file.name

    def get_absolute_url(self):
        return reverse("file_view", kwargs={"slug": self.file.slug})
