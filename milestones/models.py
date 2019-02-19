from django.db import models
from areas.models import Area


class Milestone(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    value = models.FloatField(default=0)
    secondary_value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'milestones'
