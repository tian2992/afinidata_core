from django import forms
from instances.models import Score, ScoreTracking, Instance
from attributes.models import Attribute


class ScoreModelForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('value', 'area', 'instance')


class ScoreTrackingModelForm(forms.ModelForm):

    class Meta:
        model = ScoreTracking
        fields = ('value', 'area', 'instance')


class InstanceModelForm(forms.ModelForm):

    class Meta:
        model = Instance
        fields = ('entity', 'bot', 'name', 'bot_user_id')


class InstanceAttributeValueForm(forms.Form):
    attribute = forms.ModelChoiceField(queryset=Attribute.objects.all())
    value = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset')
        super(InstanceAttributeValueForm, self).__init__(*args, **kwargs)
        self.fields['attribute'].queryset = self.queryset
