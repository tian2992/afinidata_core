from django import forms
from milestones.models import Milestone
from instances.models import Instance


class MilestoneFormModel(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ('name', 'code', 'area',  'value', 'secondary_value', 'description')


class ResponseMilestoneForm(forms.Form):
    RESPONSE_CHOICES = (
        ('true', 'yes'),
        ('false', 'no')
    )
    instance = forms.ModelChoiceField(queryset=Instance.objects.all())
    step = forms.IntegerField()
    response = forms.ChoiceField(choices=RESPONSE_CHOICES)
