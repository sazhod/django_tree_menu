from django.contrib import admin
from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('<str:menu_item>', views.index, name='home'),
    path('', views.index, name='home'),
]
