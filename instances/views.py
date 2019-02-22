from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from instances.models import Instance
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView


class HomeView(TemplateView):
    template_name = 'instances/index.html'

    def get_context_data(self, **kwargs):
        instances = Instance.objects.all()
        return dict(instances=instances)


class InstanceView(TemplateView):
    template_name = 'instances/instance.html'

    def get_context_data(self, **kwargs):
        instance = get_object_or_404(Instance, pk=kwargs['id'])

        return dict(instance=instance)


class NewInstanceView(CreateView):
    model = Instance
    template_name = 'instances/new.html'
    fields = ('entity', 'bot', 'name')

    def form_valid(self, form):
        form.save()
        return redirect('instances:index')


class EditInstanceView(UpdateView):
    model = Instance
    fields = ('entity', 'bot', 'name')
    template_name = 'instances/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'instance'

    def form_valid(self, form):
        entity = form.save()
        return redirect('instances:edit', entity.pk)


class DeleteInstanceView(DeleteView):
    model = Instance
    template_name = 'instances/delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('instances:index')
