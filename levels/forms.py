from django import forms
from levels.models import Level


class LevelModelForm(forms.ModelForm):

    class Meta:
        model = Level
        fields = ('name', 'min', 'max')