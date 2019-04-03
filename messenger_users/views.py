from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, View
from messenger_users.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os


class HomeView(LoginRequiredMixin, ListView):

    template_name = 'messenger_users/index.html'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'users'
    paginate_by = 100

    def get_queryset(self):
        return User.objects.all()


class UserCaptchaView(View):

    def get(self, request):

        try:
            username = request.GET['username']
            user = User.objects.get(username=username)
            quest = request.GET['quest']
        except Exception as e:
            return JsonResponse(dict(status='error', error='Invalid params.'))

        if quest != 'afini':
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
            quest = request.GET['quest']
        except Exception as e:
            return JsonResponse(dict(status='error', error='Invalid params.'))

        if quest != 'afini':
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
