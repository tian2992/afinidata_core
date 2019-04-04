from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, View, ListView, DetailView
from entities.models import Entity
from attributes.models import Attribute
from django.urls import reverse_lazy
from django.http import JsonResponse
from entities.forms import EntityAttributeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'entities/index.html'
    model = Entity
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'entities'


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


class AddAttributeToEntityView(View):

    def get(self, request, *args, **kwargs):
        entity = get_object_or_404(Entity, id=kwargs['id'])
        queryset = Attribute.objects.all().difference(entity.attributes.all())
        form = EntityAttributeForm(request.POST or None, queryset=queryset)
        return render(request, 'entities/add_attribute.html', dict(form=form))

    def post(self, request, *args, **kwargs):

        entity = get_object_or_404(Entity, id=kwargs['id'])
        queryset = Attribute.objects.filter(id=request.POST['attribute'])
        form = EntityAttributeForm(request.POST, queryset=queryset)

        if form.is_valid():
            attribute = Attribute.objects.get(id=request.POST['attribute'])
            entity.attributes.add(attribute)
            messages.success(request, 'Attribute has been added to entity')
            return redirect('entities:entity', id=entity.pk)
        else:
            print('invalid')
        return JsonResponse(dict(world='hello'))
