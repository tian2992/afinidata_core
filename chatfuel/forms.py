from django import forms
from instances.models import Instance
from messenger_users.models import User
from groups.models import Code


class SetSectionToInstance(forms.Form):
    instance = forms.ModelChoiceField(Instance.objects.all())
    value = forms.IntegerField()


class GetInstancesForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    label = forms.CharField(max_length=50, required=False)


class VerifyCodeForm(forms.Form):
    code = forms.ModelChoiceField(Code.objects.all(), to_field_name='code')
