from django.urls import path, re_path
from k8s import views

urlpatterns = [
    re_path('^node/$', views.node, name='node'),
    re_path('^namespace/$', views.namespace, name='namespace'),
    re_path('^namespace_api/$', views.namespace_api, name='namespace_api'),
    re_path('^node_api/$', views.node_api, name='node_api'),
]
