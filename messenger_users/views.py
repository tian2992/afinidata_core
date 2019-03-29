from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from messenger_users.models import User
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
