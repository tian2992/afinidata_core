from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from areas.forms import AreaFormModel


class HomeView(TemplateView):
    template_name = 'areas/index.html'


class NewAreaView(View):
    template_name = 'areas/new.html'

    def post(self, request, *args, **kwargs):
        form = AreaFormModel(request.POST)

        if form.is_valid():
            form.save()
            return redirect('areas:index')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = AreaFormModel(request.POST or None)

        return render(request, self.template_name, {'form': form})
