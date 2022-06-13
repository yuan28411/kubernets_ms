from django.db import models

# Create your models here.


class K8sAuth(models.Model):
    auth_type = models.CharField(max_length=30)
    token = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)
