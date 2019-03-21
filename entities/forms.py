from django import forms
from attributes.models import Attribute
from entities.models import Entity


class EntityAttributeForm(forms.Form):
    attribute = forms.ModelChoiceField(Attribute.objects.all())

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        super(EntityAttributeForm, self).__init__(*args, **kwargs)
        queryset = Attribute.objects.all().difference(self.entity.attributes.all())
        print(queryset)
        self.fields['attribute'] = forms.ModelChoiceField(queryset)


