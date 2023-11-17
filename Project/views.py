from .models import Project, ProjectsImage, ProjectsDocument
from .serializers import PostProjectSerializer, GetAllProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Subquery, OuterRef
from django.http import Http404


class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.annotate(
            first_image=Subquery(ProjectsImage.objects.filter(project_id=OuterRef('id')).values('image')[:1])
        ).values("id", "name", "price", "first_image")
        serializer = GetAllProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    def get_project_instance(self, id):
        try:
            return Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, id):
        project = self.get_project_instance(id)
        serializer = PostProjectSerializer(project, many=False)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

