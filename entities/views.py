from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from entities.models import Entity
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = 'entities/index.html'

    def get_context_data(self, **kwargs):
        entities = Entity.objects.all()
        return dict(entities=entities)


class EntityView(TemplateView):
    template_name = 'entities/entity.html'

    def get_context_data(self, **kwargs):
        entity = get_object_or_404(Entity, pk=kwargs['id'])

        return dict(entity=entity)


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


class DeleteEntityView(DeleteView):
    model = Entity
    template_name = 'entities/delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('entities:index')
