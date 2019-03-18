from django.shortcuts import render
from django.views.generic import TemplateView
from messenger_users.models import User


class HomeView(TemplateView):

    template_name = 'messenger_users/index.html'

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        print(users)
        return dict(users=users)
