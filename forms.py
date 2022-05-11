from django import forms

from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ["name", "user", "slug", "type"]
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "type": "textarea",
                    "class": "form-control",
                    "id": "textaria",
                    "aria-describedby": "basic-addon3",
                }
            ),
            "file": forms.FileInput(
                attrs={
                    "type": "file",
                    "class": "form-control",
                    "id": "file",
                    "aria-describedby": "basic-addon3",
                    "name": "file",
                    "multiple": "true",
                }
            ),
        }
