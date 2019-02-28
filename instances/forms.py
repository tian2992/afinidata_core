from django.forms import ModelForm
from instances.models import Score, ScoreTracking, Instance


class ScoreModelForm(ModelForm):

    class Meta:
        model = Score
        fields = ('value', 'area', 'instance')


class ScoreTrackingModelForm(ModelForm):

    class Meta:
        model = ScoreTracking
        fields = ('value', 'area', 'instance')


class InstanceModelForm(ModelForm):

    class Meta:
        model = Instance
        fields = ('entity', 'bot', 'name', 'bot_user_id')
