from django import forms
from attributes.models import Attribute
from entities.models import Entity


class EntityAttributeForm(forms.Form):
    attribute = forms.ModelChoiceField(Attribute.objects.all())

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset')
        super(EntityAttributeForm, self).__init__(*args, **kwargs)
        self.fields['attribute'] = forms.ModelChoiceField(queryset=self.queryset)