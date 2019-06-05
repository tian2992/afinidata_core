from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone


class HomeView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        return dict(today=timezone.now())
