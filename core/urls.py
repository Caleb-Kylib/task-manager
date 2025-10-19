"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from .views import home

#  Import the RegisterView from your users app
from users.views import RegisterView

#  Import JWT views from SimpleJWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

API_TITLE = "Task Manager API"
API_DESCRIPTION = "A simple task management API with authentication and ownership controls."

urlpatterns = [
                        
    path('admin/', admin.site.urls),      # Admin routes
    path('', home, name='home'),

    #  Add user registration route
    path('api/register/', RegisterView.as_view(), name='register'),
    
    #  JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # task app routes
    path('api/', include('tasks.urls')),    #API routes for tasks app
     
    # DRF Browsable API login
    path('api-auth/', include('rest_framework.urls')),


    # API Documentation
    path('schema/', get_schema_view(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version="1.0.0"
    ), name='openapi-schema'),

    #path('docs/', include_docs_urls(
     #   title=API_TITLE,
      #  description=API_DESCRIPTION
    #)),
]

