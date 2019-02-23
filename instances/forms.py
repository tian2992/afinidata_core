from django.forms import ModelForm
from instances.models import Score, ScoreTracking


class ScoreModelForm(ModelForm):

    class Meta:
        model = Score
        fields = ('value', 'area', 'instance')


class ScoreTrackingModelForm(ModelForm):

    class Meta:
        model = ScoreTracking
        fields = ('value', 'area', 'instance')
