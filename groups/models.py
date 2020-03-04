from django.contrib.auth.models import User
from django.db import models


ROLE_CHOICES = (('administrator', 'Administrator'), ('collaborator', 'Collaborator'))


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    users = models.ManyToManyField(User, through='RoleGroupUser')


class RoleGroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)