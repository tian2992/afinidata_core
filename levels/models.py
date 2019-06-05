from django.db import models


class Level(models.Model):
    name = models.CharField(max_length=50)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=99999)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
