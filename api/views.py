from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from file.api.serializers import FileSerializer, FileUploadSerializer
from file.models import File


class FileList(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class UploadFileViewSet(GenericViewSet):
    serializer_class = FileUploadSerializer

    @action(detail=True, methods=["POST"], queryset=File.objects.select_related("file"))
    def file(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_201_CREATED)
