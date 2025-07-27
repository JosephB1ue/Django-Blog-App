"""
URL configuration for Django_Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog_app.views import post_list_page, post_detail_page



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog_app.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', post_list_page, name='post-list-page'),
    path('view/posts/<int:post_id>/', post_detail_page, name='post-detail-page'),
]
