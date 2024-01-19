from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes

from django.http import Http404
from django.db.models import Q

from .models import Project
from .serializers import PostProjectSerializer, GetAllProjectSerializer, PutProjectSerializer
from .paginatiors import CustomPaginator


class ProjectList(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    # using custom way to paginate the response
    pagination_class = CustomPaginator

    # permission configuration, if the user is authenticated, they can both get and post projects else they can only view projects
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        category_filter = request.query_params.getlist('category', [])
        technology_filter = request.query_params.getlist('tech', [])
        price_min_filter = request.query_params.get('priceMin')
        price_max_filter = request.query_params.get('priceMax')
        ordering_filter = request.query_params.getlist('ordering', [])
        
        ordering_fields = ['price', '-price']

        for filter in ordering_filter:
            if filter not in ordering_fields:
                return Response({
                    "message": "Invalid ordering fields!!"
                }, status=400)

        # creating data filter to filter response and get the user the desired result
        filter_condition = Q()

        # data can be filtered using the "category", "tech", "priceMin" and "priceMax" attributes
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

        if ordering_filter:
            for filter in ordering_filter:
                projects.order_by(filter)

        # paginating the data
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset=projects, request=request)
        serializer = GetAllProjectSerializer(paginated_queryset, many=True)
        data = paginator.get_paginated_response(data=serializer.data)
        return data


    def post(self, request):
        serializer = PostProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):

    # authentication configuration, if the user is authenticated, then only they can view, edit or delete any project, else no ops is allowed
    # authentication_classes = [IsAuthenticated]

    def get_project_instance(self, id):
        try:
            return Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, id):
        project = self.get_project_instance(id)
        serializer = PostProjectSerializer(project, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id):
        project = self.get_project_instance(id)
        data_to_update = PutProjectSerializer(data=request.data, partial=True)
        if data_to_update.is_valid():
            updated_data = data_to_update.update(project, data_to_update.validated_data)
            serialized_data = PutProjectSerializer(updated_data).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response(data_to_update.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        project = self.get_project_instance(id)
        # Project.objects.filter(id=project.id).delete()
        # return Response({'name': f'{project.name}', 'message': 'Project deleted successfully'}, status=status.HTTP_200_OK)
        project.delete()
        return Response({'name': f'{project.name}', 'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
