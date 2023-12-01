from rest_framework import serializers
from .models import Project, ProjectsDocument, ProjectsImage, ApplicationType, TechStack


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
        fields = ["id", "name", "price", "description", "images", "uploaded_images", "documents", "uploaded_documents",
                  "application_type", "tech_stack"]
        # depth = 1

    def validate_application_type(self, data):
        if len(data) > 3:
            raise serializers.ValidationError("Chosen application type can't be more than 3")
        return data

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        uploaded_documents = validated_data.pop("uploaded_documents")
        uploaded_application_type = validated_data.pop("application_type")
        uploaded_tech_stack = validated_data.pop("tech_stack")

        project = Project.objects.create(**validated_data)

        for image in uploaded_images:
            ProjectsImage.objects.create(project=project, image=image)
        for document in uploaded_documents:
            ProjectsDocument.objects.create(project=project, document=document)
        for application_type in uploaded_application_type:
            project.application_type.add(application_type)
        for tech_stack in uploaded_tech_stack:
            project.tech_stack.add(tech_stack)

        return project


class GetAllProjectSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'price', 'first_image']

    def get_first_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None


class PutProjectSerializer(serializers.ModelSerializer):
    images = ProjectsImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    documents = ProjectsDocumentSerializer(many=True, read_only=True)
    uploaded_documents = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    deleted_images = serializers.ListField(
        child=serializers.CharField(allow_blank=True, trim_whitespace=True),
        write_only=True, required=False
    )

    deleted_documents = serializers.ListField(
        child=serializers.CharField(allow_blank=True, trim_whitespace=True),
        write_only=True, required=False
    )

    class Meta:
        model = Project
        fields = ["id", "name", "price", "description", "images", "uploaded_images", "documents", "uploaded_documents",
                  "application_type", "tech_stack", 'deleted_images', 'deleted_documents']
        # depth = 1

    def validate_application_type(self, data):
        if len(data) > 3:
            raise serializers.ValidationError("Chosen application type can't be more than 3")
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.price = validated_data['price']

        if 'uploaded_images' in validated_data:
            for image in validated_data['uploaded_images']:
                ProjectsImage.objects.create(project=instance, image=image)

        if 'uploaded_documents' in validated_data:
            for docs in validated_data['uploaded_documents']:
                ProjectsDocument.objects.create(project=instance, document=docs)

        if 'deleted_images' in validated_data:
            for deleted_image in validated_data['deleted_images']:
                ProjectsImage.objects.filter(project_id=instance.id).filter(image=deleted_image).delete()

        if 'deleted_documents' in validated_data:
            for deleted_document in validated_data['deleted_documents']:
                ProjectsDocument.objects.filter(project_id=instance.id).filter(image=deleted_document).delete()

        instance.tech_stack.clear()

        for tech in validated_data['tech_stack']:
            instance.tech_stack.add(tech.id)

        instance.application_type.clear()

        for category in validated_data['application_type']:
            instance.application_type.add(category.id)

        instance.save()
        return instance
