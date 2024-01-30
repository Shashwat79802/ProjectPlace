from django.urls import path
from .views import SignUpView, LoginView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register-user'),
    path('update-user/', SignUpView.as_view(), name='update-user'),
    path('login/', LoginView.as_view(), name='login-user'),
]