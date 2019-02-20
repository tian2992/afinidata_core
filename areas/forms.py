from django import forms
from areas.models import Area


class AreaFormModel(forms.ModelForm):

    class Meta:
        model = Area
        fields = ['name', 'description']
