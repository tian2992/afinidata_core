from instances.forms import ScoreModelForm, InstanceModelForm
from messenger_users.models import User as MessengerUser
from instances.models import Instance, InstanceSection
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from milestones.forms import ResponseMilestoneForm
from django.views.generic import View, CreateView
from messenger_users.models import User, UserData
from chatfuel.forms import SetSectionToInstance
from milestones.models import Milestone
from areas.models import Area, Section
from django.http import JsonResponse
from django.conf import settings
from groups.models import Code
from chatfuel import forms
import requests


@method_decorator(csrf_exempt, name='dispatch')
class CreateMessengerUserView(CreateView):
    model = User
    fields = ('channel_id', 'bot_id')

    def form_valid(self, form):
        form.instance.last_channel_id = form.data['channel_id']
        form.instance.username = form.data['channel_id']
        form.instance.backup_key = form.data['channel_id']
        user = form.save()
        return JsonResponse(dict(set_attributes=dict(user_id=user.pk, request_status='done'), messages=[]))

    def form_invalid(self, form):
        user_set = User.objects.filter(channel_id=form.data['channel_id'])
        if user_set.count() > 0:
            return JsonResponse(dict(set_attributes=dict(user_id=user_set.last().pk,
                                                         request_status='done'), messages=[]))

        return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                     request_message='Invalid params'), messages=[]))


@method_decorator(csrf_exempt, name='dispatch')
class CreateMessengerUserDataView(CreateView):
    model = UserData
    fields = ('user', 'data_key', 'data_value')

    def form_valid(self, form):
        form.save()
        return JsonResponse(dict(set_attributes=dict(request_status='done'), messages=[]))

    def form_invalid(self, form):
        return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                     request_message='Invalid params'), messages=[]))


@method_decorator(csrf_exempt, name='dispatch')
class GetInstancesByUserView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(dict(set_attributes=dict(request_status='error', request_error='Invalid Method'),
                                 messages=[]))

    def post(self, request):
        form = forms.GetInstancesForm(request.POST)

        if not form.is_valid():
            return JsonResponse(dict(set_attributes=dict(request_status='error', request_error='Invalid Method'),
                                     messages=[]))

        label = "Choice your instance: "
        try:
            if form.data['label']:
                label = form.data['label']
        except:
            pass
        user = MessengerUser.objects.get(id=int(form.data['user']))
        replies = [dict(title=item.name, set_attributes=dict(instance=item.pk, instance_name=item.name)) for item in
                   user.get_instances()]

        return JsonResponse(dict(
            set_attributes=dict(request_status='done'),
            messages=[
                dict(
                    text=label,
                    quick_replies=replies
                )
            ]
        ))


@csrf_exempt
def create_instance(request):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error="Invalid method."))

    form = InstanceModelForm(request.POST)

    if not form.is_valid():
        return JsonResponse(dict(status="error", error="Invalid params."))

    new_instance = form.save()

    return JsonResponse(dict(
        set_attributes=dict(
            instance=new_instance.pk,
            instance_name=new_instance.name
        ),
        messages=[]
    ))


@method_decorator(csrf_exempt, name='dispatch')
class VerifyCodeView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(dict(request_status='error', request_error='Invalid Method'))

    def post(self, request):
        form = forms.VerifyCodeForm(request.POST)
        if not form.is_valid():
            return JsonResponse(dict(set_attributes=dict(request_status='error', request_error='Invalid params'),
                                     messages=[]))

        code = Code.objects.get(code=form.data['code'])

        return JsonResponse(dict(set_attributes=dict(request_status='done', request_code=code.code,
                                                     request_code_group=code.group.name),
                                 messages=[]))
