from rest_framework import serializers
from .models import Project, ProjectsDocument, ProjectsImage


class ProjectsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsImage
        fields = "__all__"


class ProjectsDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsDocument
        fields = "__all__"


class PostProjectSerializer(serializers.ModelSerializer):
    images = ProjectsImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    documents = ProjectsDocumentSerializer(many=True, read_only=True)
    uploaded_documents = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Project
        fields = ["id", "name", "price", "description", "images", "uploaded_images", "documents", "uploaded_documents"]
        # fields = ["id", "name", "price", "description", "uploaded_images", "uploaded_documents"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        uploaded_documents = validated_data.pop("uploaded_documents")

        project = Project.objects.create(**validated_data)

        for image in uploaded_images:
            ProjectsImage.objects.create(project=project, image=image)
        for document in uploaded_documents:
            ProjectsDocument.objects.create(project=project, document=document)

        return project


class GetAllProjectSerializer(serializers.ModelSerializer):
    first_image = serializers.FilePathField(read_only=True, path='/media')

    class Meta:
        model = Project
        fields = ['id', 'name', 'price', 'first_image']


# class GetProjectSerializer(ser)