"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from .views import home

API_TITLE = "Task Manager API"
API_DESCRIPTION = "A simple task management API with authentication and ownership controls."

urlpatterns = [
                        
    path('admin/', admin.site.urls),      # Admin rou
    path('', home, name='home'),


    # Include task app routes
    path('api/', include('tasks.urls')),    #API routes for tasks app

    # Optional API documentation (you can comment these out if you don't need them)
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

