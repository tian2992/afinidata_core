from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, DetailView, UpdateView, DeleteView
from messenger_users.models import User, UserData
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib import messages
from instances.models import Instance
import random
import os


class HomeView(LoginRequiredMixin, ListView):

    template_name = 'messenger_users/index.html'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'users'
    paginate_by = 100
    model = User


class UserView(LoginRequiredMixin, DetailView):
    model = User
    pk_url_kwarg = 'id'
    context_object_name = 'user'
    template_name = 'messenger_users/user.html'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        user_id = kwargs['object'].pk
        instances = Instance.objects.filter(user_id=user_id)
        return dict(user=kwargs['object'], instances=instances)


class UserCaptchaView(View):

    def get(self, request):

        try:
            username = request.GET['username']
            user = User.objects.get(username=username)
            api_key = request.GET['api_key']
        except Exception as e:
            return JsonResponse(dict(status='error', error='Invalid params.'))

        if api_key != os.getenv('CORE_QUEST_KEY'):
            return JsonResponse(dict(status='error', error='Invalid params.'))

        captcha = '00%sCHF' % user.id

        return JsonResponse(dict(
            set_attributes=dict(
                captcha=captcha,
                core_message='Captcha for user %s is %s' % (user.username, captcha)
            ),
            messages=[]
        ))


class VerifyUserCaptchaView(View):

    def get(self, request):

        try:
            user = User.objects.get(username=request.GET['username'])
            response = str(request.GET['response'])
            api_key = request.GET['api_key']
        except Exception as e:
            return JsonResponse(dict(status='error', error='Invalid params.'))

        if api_key != os.getenv('CORE_QUEST_KEY'):
            return JsonResponse(dict(status='error', error='Invalid params.'))

        captcha = '00%sCHF' % user.id

        if response == captcha:
            valid_captcha = True
            core_message = 'Captcha valid'
        else:
            valid_captcha = False
            core_message = 'Captcha invalid'

        return JsonResponse(dict(
            set_attributes=dict(
                valid_captcha=valid_captcha,
                core_message=core_message
            ),
            messages=[]
        ))


class DataView(View):

    def get(self, request):
        try:
            admin = request.GET['admin']
            password = request.GET['password']
            username = request.GET['username']
            user = User.objects.get(username=username)
        except Exception as e:
            return JsonResponse(dict(status='error', error='invalid params'))

        if admin != os.getenv('CORE_ADMIN_ADMIN') or password != os.getenv('CORE_ADMIN_PASSWORD'):
            return HttpResponse('Admin o contraseña incorrecta')

        dataset = user.userdata_set.all()

        text = 'Data for %s is: \n' % user.username

        for item in dataset:
            text = text + "%s: %s \n" % (item.data_key, item.data_value)
        return HttpResponse(text)


class DeleteByUsernameView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'messenger_users/username.html', {})

    def post(self, request):
        user = get_object_or_404(User, username=request.POST['username'])
        user.delete()
        return redirect('messenger_users:index')


@csrf_exempt
def set_attributes_for_user(request, id):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error='Invalid method.'))

    try:
        user = User.objects.get(id=id)
    except Exception as e:
        return JsonResponse(dict(status='error', error='invalid params.'))

    for data_key in request.POST:
        data_value = request.POST[data_key]
        new_data = UserData.objects.update_or_create(user=user, data_key=data_key, defaults=dict(
            data_value=data_value
        ))
        print(new_data)
    return JsonResponse(dict(hello='world'))


class SetRandomPostGroupForUser(View):

    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=kwargs['id'])
        except Exception as e:
            return JsonResponse(status='error', error='Invalid params.')

        random_choices = ['random', 'ranking', 'feedback']
        data_value = random.choice(random_choices)
        data_key = 'posts_group'

        new_attribute = user.userdata_set.update_or_create(data_key=data_key, defaults=dict(
            data_value=data_value
        ))
        print(new_attribute)
        return JsonResponse(dict(status='done', data=dict(data_key=data_key, data_value=data_value,
                                                          user_id=user.pk,
                                                          set_attributes=dict(
                                                              posts_group=data_value
                                                          ),
                                                          messages=[])))


class EditAttributeView(LoginRequiredMixin, UpdateView):
    model = UserData
    pk_url_kwarg = 'attribute_id'
    fields = ('data_value',)
    template_name = 'messenger_users/data_edit.html'
    context_object_name = 'data'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def get_object(self, queryset=None):
        object = get_object_or_404(UserData, user_id=self.kwargs['id'], id=self.kwargs['attribute_id'])
        return object

    def form_valid(self, form):
        data = form.save()
        messages.success(self.request, 'Attribute with name: %s has been updated' % data.data_key)
        return redirect('messenger_users:user', id=self.kwargs['id'])


class DeleteAttributeView(LoginRequiredMixin, DeleteView):
    model = UserData
    pk_url_kwarg = 'attribute_id'
    template_name = 'messenger_users/data_delete.html'
    context_object_name = 'data'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('messenger_users:index')

    def get_object(self, queryset=None):
        object = get_object_or_404(UserData, user_id=self.kwargs['id'], id=self.kwargs['attribute_id'])
        return object


class GetIDByUsernameView(View):

    def get(self, request):
        try:
            api_key = request.GET['api_key']
            username = request.GET['username']
            user = User.objects.get(username=username)
            print(user)
            print(os.getenv('CORE_QUEST_KEY'))
        except Exception as e:
            print(str(e))
            return JsonResponse(dict(status='error', error="Invalid params."))