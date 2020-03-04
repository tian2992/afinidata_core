from django.contrib.auth.models import User
from messenger_users.models import User as MessengerUser
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


class Code(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    available = models.BooleanField(default=True)
    exchanges = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class AssignationMessengerUser(models.Model):
    messenger_user_id = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code_id = models.ForeignKey(Code, null=True, on_delete=models.SET_NULL)

    def get_messenger_user(self):
        return MessengerUser.objects.get(id=self.messenger_user_id)
