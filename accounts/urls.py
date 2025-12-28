"""
accounts/urls.py
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import RegisterView, LoginView, LogoutView, UserProfileView, ChangePasswordView

@api_view(['GET'])
def auth_root(request, format=None):
    """
    API root view for authentication endpoints
    """
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'token_refresh': reverse('token_refresh', request=request, format=format),
        'profile': reverse('profile', request=request, format=format),
        'change_password': reverse('change_password', request=request, format=format),
    })

urlpatterns = [
    path('', auth_root, name='auth-root'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]