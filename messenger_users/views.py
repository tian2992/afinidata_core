from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View
from messenger_users.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):

    template_name = 'messenger_users/index.html'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'users'
    paginate_by = 50

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