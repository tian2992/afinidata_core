from django import forms
from areas.models import Area


class AreaFormModel(forms.ModelForm):

    class Meta:
        model = Area
        fields = ['name', 'description']


class MilestonesByAreaForm(forms.Form):
    TYPE_CHOICES = (
        ('increment', 'INCREMENT'),
        ('decrement', 'DECREMENT')
    )
    value = forms.IntegerField()
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    step = forms.IntegerField()
