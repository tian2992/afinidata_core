from django import forms
from milestones.models import Milestone


class MilestoneFormModel(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ('area', 'name', 'value', 'secondary_value')
