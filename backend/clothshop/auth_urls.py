from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import auth_views

urlpatterns = [
    path('login/', auth_views.login_view, name='api_login'),
    path('logout/', auth_views.logout_view, name='api_logout'),
    path('whoami/', auth_views.whoami, name='api_whoami'),
    path('register/', auth_views.register_view, name='api_register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
