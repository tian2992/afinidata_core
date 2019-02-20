from django import forms
from milestones.models import Milestone


class MilestoneFormModel(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ('name', 'code', 'area',  'value', 'secondary_value', 'description')
