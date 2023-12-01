from django.urls import path
from .views import ProjectList, ProjectDetail

urlpatterns = [
    path("project/", ProjectList.as_view(), name="list_Project"),
    path("project/<uuid:id>", ProjectDetail.as_view(), name="detail_Project")
]
