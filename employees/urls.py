from django.urls import path

from . import views

urlpatterns = [
    path('', views.department_tree, name='department_tree'),
]
