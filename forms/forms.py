from django import forms
from attributes.models import Attribute


class FormAttributeForm(forms.Form):
    distinct_of = forms.CharField(max_length=255, required=False)
    match_with = forms.CharField(max_length=255, required=False)
    attribute = forms.ModelChoiceField(Attribute.objects.all())

    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop('form')
        super(FormAttributeForm, self).__init__(*args, **kwargs)
        attributes = self.form.entity.attributes.all().difference(self.form.attributes.all())
        self.fields['attribute'] = forms.ModelChoiceField(attributes)
