from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, CreateView
from entities.models import Entity


class HomeView(TemplateView):
    template_name = 'entities/index.html'

    def get_context_data(self, **kwargs):
        entities = Entity.objects.all()
        return dict(entities=entities)


class NewEntityView(CreateView):
    model = Entity
    template_name = 'entities/new.html'
    fields = ('name', 'description')

    def form_valid(self, form):
        form.save()
        return redirect('entities:index')


class EditEntityView(UpdateView):
    model = Entity
    fields = ('name', 'description')
    template_name = 'entities/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'entity'

    def form_valid(self, form):
        entity = form.save()
        return redirect('entities:edit', entity.pk)