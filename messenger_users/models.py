from instances import models as InstanceModels
from bots.models import Bot
from django.db import models
import uuid


class User(models.Model):
    last_channel_id = models.CharField(max_length=50, unique=True)
    channel_id = models.CharField(max_length=50, null=True, unique=True)
    backup_key = models.CharField(max_length=50, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bot_id = models.IntegerField(default=1)
    username = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.username

    def get_first_name(self):
        try:
            return self.userdata_set.get(data_key='channel_first_name').data_value
        except:
            return None

    def get_last_name(self):
        try:
            return self.userdata_set.get(data_key='channel_last_name').data_value
        except:
            return None

    def get_instances(self):
        return InstanceModels.Instance.objects.filter(user_id=self.pk)

    def get_bot(self):
        return Bot.objects.get(id=self.bot_id)

    def get_email(self):
        keys = self.userdata_set.filter(data_key='email')
        print(keys)
        if keys.count() > 0:
            return keys.last().data_value
        else:
            return None

    def get_country(self):
        keys = self.userdata_set.filter(data_key='Pais')
        print(keys)
        if keys.count() > 0:
            return keys.last().data_value
        else:
            return None

    def get_property(self, data_key):
        keys = self.userdata_set.filter(data_key=data_key)
        print(keys)
        if keys.count() > 0:
            return keys.last().data_value
        else:
            return None


class UserData(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    data_key = models.CharField(max_length=30)
    data_value = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.data_value


class Child(models.Model):
    parent_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    dob = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now=True)


class ChildData(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    data_key = models.CharField(max_length=50)
    data_value = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.pk


class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_shared = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='shared_ref')
    user_opened = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='opened_ref', null=True)
    ref_type = models.CharField(choices=[("link", "link"), ("ref","ref")], default="link", max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User '{}' referred '{}'".format(self.user_shared, self.user_opened)
