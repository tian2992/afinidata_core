from django.db import models
from entities.models import Entity
from attributes.models import Attribute


class Form(models.Model):
    entity = models.ForeignKey(to=Entity, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    attributes = models.ManyToManyField(Attribute, through='Validation')

    def __str__(self):
        return self.name


class Validation(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    min = models.CharField(max_length=255, null=True)
    max = models.CharField(max_length=255, null=True)
    distinct_of = models.CharField(max_length=255, null=True)
    match_with = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s__%s__%s" % (self.pk, self.form.name, self.attribute.name)
