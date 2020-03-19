from instances.models import InstanceAssociationUser, Instance, AttributeValue, PostInteraction
from django.views.generic import View, CreateView, TemplateView, UpdateView
from groups.models import Code, AssignationMessengerUser
from messenger_users.models import User as MessengerUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from messenger_users.models import User, UserData
from django.http import JsonResponse, Http404
from attributes.models import Attribute
from groups import forms as group_forms
from chatfuel import forms
from django.utils import timezone


''' MESSENGER USERS VIEWS '''


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
                                                         request_status='error', request_message='User exists'),
                                     messages=[]))

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


''' INSTANCES VIEWS '''


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
        return JsonResponse(dict(
            set_attributes=dict(request_status='error', request_error='Invalid Method'),
            messages=[]
        ))

    form = forms.InstanceModelForm(request.POST)

    if not form.is_valid():
        return JsonResponse(dict(
            set_attributes=dict(request_status='error', request_error='Invalid Params'),
            messages=[]
        ))

    new_instance = form.save()
    assignation = InstanceAssociationUser.objects.create(user_id=form.data['user_id'], instance=new_instance)

    return JsonResponse(dict(
        set_attributes=dict(
            request_status='done',
            instance=new_instance.pk,
            instance_name=new_instance.name,
            instance_assignation_id=assignation.pk
        ),
        messages=[]
    ))


@method_decorator(csrf_exempt, name='dispatch')
class GetInstanceAttributeView(TemplateView):
    template_name = 'chatfuel/form.html'

    def get_context_data(self, **kwargs):
        c = super(GetInstanceAttributeView, self).get_context_data()
        c['form'] = forms.GetInstanceAttributeValue(None)
        return c

    def post(self, request, *args, **kwargs):
        form = forms.GetInstanceAttributeValue(self.request.POST)

        if not form.is_valid():
            return JsonResponse(dict(set_attributes=dict(request_status='error', request_error='Invalid params'),
                                     messages=[]))

        instance = Instance.objects.get(id=form.data['instance'])
        attributes = instance.entity.attributes.filter(name=form.data['attribute'])

        if not attributes.count() > 0:
            return JsonResponse(dict(set_attributes=dict(
                request_status='error',
                request_error='Entity of instance has not attribute with name %s.' % form.data['attribute']),
                                     messages=[]))

        attribute = Attribute.objects.get(name=form.data['attribute'])
        instance_attributes = AttributeValue.objects.filter(attribute=attribute, instance=instance)

        if not instance_attributes.count() > 0:
            return JsonResponse(dict(set_attributes=dict(
                request_status='error',
                request_error='Instance has not values with attribute: %s.' % form.data['attribute']),
                messages=[]))

        return JsonResponse(
            dict(set_attributes={
                'request_status': 'done',
                form.data['attribute']: instance_attributes.last().value
            },
                 messages=[])
        )


@method_decorator(csrf_exempt, name='dispatch')
class ChangeInstanceNameView(TemplateView):
    template_name = 'chatfuel/form.html'

    def get_context_data(self, **kwargs):
        c = super(ChangeInstanceNameView, self).get_context_data()
        c['form'] = forms.ChangeNameForm(None)
        print(c['form'])
        return c

    def post(self, request, *args, **kwargs):

        form = forms.ChangeNameForm(self.request.POST)

        if not form.is_valid():
            return JsonResponse(dict(set_attributes=dict(
                request_status='error',
                request_error='Invalid Params.'
            ), messages=[]))

        instance = Instance.objects.get(id=form.data['instance'])
        instance.name = form.data['name']
        response = instance.save()

        return JsonResponse(dict(set_attributes=dict(
            request_status='done',
            request_message="name for instance has been changed.",
            instance_name=instance.name
        ), messages=[]))


''' CODE VIEWS '''


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


@method_decorator(csrf_exempt, name='dispatch')
class ExchangeCodeView(TemplateView):
    template_name = 'groups/code_form.html'

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        form = group_forms.ExchangeCodeForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['messenger_user_id']
            code = form.cleaned_data['code']
            changes = AssignationMessengerUser.objects.filter(messenger_user_id=user.pk)
            print(changes)
            if not changes.count() > 0:
                exchange = AssignationMessengerUser.objects.create(messenger_user_id=user.pk, group=code.group,
                                                                   code=code)
                code.exchange()
                return JsonResponse(dict(set_attributes=dict(request_status='done'), messages=[]))
            else:
                return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                             request_error='User be in group'), messages=[]))
        else:
            return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                         request_error='User ID or code wrong'), messages=[]))


@method_decorator(csrf_exempt, name='dispatch')
class CreateInstanceAttributeView(CreateView):
    model = AttributeValue
    template_name = 'chatfuel/form.html'
    fields = ('instance', 'value', 'attribute')

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_form(self, form_class=None):
        form = super(CreateInstanceAttributeView, self).get_form(form_class=None)
        form.fields['attribute'].to_field_name = 'name'
        return form

    def form_valid(self, form):

        if not form.instance.instance.entity.attributes.filter(id=form.instance.attribute.pk):
            return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                         error_message='Attribute not in instance'), messages=[]))

        attribute_value = form.save()

        return JsonResponse(dict(set_attributes=dict(
            set_attributes=dict(request_status='done', request_attribute_value_id=attribute_value.pk),
            messages=[]
        )))

    def form_invalid(self, form):
        return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                     status_error='Invalid params'), messages=[]))

    def get(self, request, *args):
        raise Http404


''' INTERACTION VIEWS '''


@method_decorator(csrf_exempt, name='dispatch')
class CreateInstanceInteractionView(CreateView):
    template_name = 'chatfuel/form.html'
    form_class = forms.InstanceInteractionForm

    def form_valid(self, form):
        form.instance.post_id = form.data['post_id']
        form.instance.created_at = timezone.now()
        interaction = form.save()

        if not interaction:
            return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                         status_error='Invalid params'), messages=[]))

        return JsonResponse(dict(set_attributes=dict(request_status='done',
                                                     request_interaction_id=interaction.pk),
                                 messages=[]))

    def form_invalid(self, form):
        return JsonResponse(dict(set_attributes=dict(request_status='error',
                                                     status_error='Invalid params'), messages=[]))

