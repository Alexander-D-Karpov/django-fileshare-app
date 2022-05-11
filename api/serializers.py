from rest_framework import serializers
from file.models import File, Group, GroupFile
from user.models import Person
from secrets import compare_digest
from site_blog import settings


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["name", "description", "user", "file", "date", "slug", "type"]

    id = serializers.ManyRelatedField


class FileUploadSerializer(serializers.ModelSerializer):
    class SecretSerializer(serializers.Serializer):
        secret = serializers.CharField()

    class UserAndGroupSerializer(serializers.Serializer):
        username = serializers.CharField()
        group_name = serializers.CharField(allow_null=True)

    secret = SecretSerializer()
    user_data = UserAndGroupSerializer()

    class Meta:
        model = File
        fields = ["file", "secret", "user_data"]

    def validate(self, data):
        secret = data["secret"]["secret"]
        username = data["user_data"]["username"]
        group_name = data["user_data"]["group_name"]
        file = data["file"]

        if not compare_digest(
            secret, "BibaBibaBibaBibaBiba-3i4x7tiyt@#T435uyeg324tue54rweyi234uxi"
        ):
            raise serializers.ValidationError("secret token is not correct")

        if not Person.objects.filter(username=username).exists():
            raise serializers.ValidationError("user doesnt exist")

        name = file.name
        file = File(
            name=name,
            user=Person.objects.get(username=username),
            description=f"{name} uploaded from computer by {username}",
            file=file,
        )
        file.gen_file()

        if group_name:
            if Group.objects.filter(name=group_name).exists():
                GroupFile.objects.create(
                    group_id=Group.objects.get(name=group_name).id, file_id=file.id
                )
            else:
                group = Group(name=group_name, private=True)
                group.save()
                GroupFile.objects.create(group=group, file_id=file.id)
        return file

    def create(self, validated_data):
        return validated_data["file"]

    id = serializers.ManyRelatedField
