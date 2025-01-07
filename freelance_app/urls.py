from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import register, jobs, user

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),

    # User endpoints
    path('users/<int:user_id>', user, name='user'),

    # Job endpoints
    path('jobs', jobs, name='jobs_list'),
    path('jobs/<int:job_id>', jobs, name='job_delete'),
]