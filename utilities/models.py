from django.db import models


class InteractionInstanceMigrations(models.Model):
    date = models.DateTimeField(auto_now=True)
    last_register_id = models.IntegerField(default=0)
    qty_register = models.IntegerField(default=0)
    last_data_id = models.IntegerField()
