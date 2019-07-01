from django import forms
from instances.models import Instance


class SetSectionToInstance(forms.Form):
    instance = forms.ModelChoiceField(Instance.objects.all())
    value = forms.IntegerField()
