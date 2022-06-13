from django.urls import path, re_path
from workload import views

urlpatterns = [
    path('deployment/', views.deployment, name='deployment'),
]
