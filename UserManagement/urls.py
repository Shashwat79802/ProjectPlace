from django.urls import path
from .views import UserView

urlpatterns = [
    path('register/', UserView.as_view(), name='register-user'),
    path('update-details/', UserView.as_view(), name='update-user'),
]