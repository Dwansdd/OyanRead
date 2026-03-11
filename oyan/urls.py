"""
URL configuration for oyan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from catalog.views import index
from catalog import views
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from catalog.views import ArticlesViewSet,Search
router = DefaultRouter()
router.register(r'articles', ArticlesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('allarticles/', views.archive_articleslist.as_view(), name='archive_articles'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('allarticles/load/',views.article_view_api, name='article_api'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('addarticle/', views.FormView, name='add_article'),
    path('registration/', views.ReigisterForm, name='rega'),
    path('search/',Search.as_view(), name='search'),
    path('add/',views.article_add_view_api, name='extra')
]