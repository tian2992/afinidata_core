from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from levels.models import Level
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages


class ListLevelView(ListView):
    template_name = 'levels/index.html'
    queryset = Level.objects.all()
    context_object_name = 'levels'


class LevelView(TemplateView):
    template_name = 'levels/level.html'

    def get_context_data(self, **kwargs):
        level = get_object_or_404(Level, id=kwargs['id'])
        return dict(level=level)


class CreateLevelView(CreateView):
    model = Level
    template_name = 'levels/new.html'
    fields = ('name', 'min', 'max')

    def form_valid(self, form):
        level = form.save()
        messages.success(self.request, 'Level with name: "%s" has been created' % level.name)
        return redirect('levels:index')


class UpdateLevelView(UpdateView):
    template_name = 'levels/edit.html'
    model = Level
    fields = ('name', 'min', 'max')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        level = form.save()
        messages.success(self.request, 'Level with name %s has been updated' % level.name)
        return redirect('levels:index')
