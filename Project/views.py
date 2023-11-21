from .models import Project, ProjectsImage, ProjectsDocument
from .serializers import PostProjectSerializer, GetAllProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.db.models import Q
from .paginatiors import CustomPaginator


class ProjectList(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    pagination_class = CustomPaginator

    def get(self, request):
        category_filter = request.query_params.getlist('category', [])
        technology_filter = request.query_params.getlist('tech', [])
        price_min_filter = request.query_params.get('priceMin')
        price_max_filter = request.query_params.get('priceMax')

        filter_condition = Q()

        if category_filter:
            filter_condition &= Q(application_type__category__in=category_filter)
        if technology_filter:
            filter_condition &= Q(tech_stack__technology__in=technology_filter)
        if price_min_filter or price_max_filter:
            price_min_filter = price_min_filter if price_min_filter is not None else 500
            price_max_filter = price_max_filter if price_max_filter is not None else 999999
            filter_condition &= Q(price__range=(price_min_filter, price_max_filter))

        if filter_condition:
            projects = Project.objects.filter(filter_condition).distinct()
            if not projects: # if no projects are found after applying the filter, raise not found error
                raise Http404
        else:
            projects = Project.objects.all()

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset=projects, request=request)
        serializer = GetAllProjectSerializer(paginated_queryset, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        data = paginator.get_paginated_response(data=serializer.data)
        return data


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
        return Response(serializer.data, status=status.HTTP_200_OK)
