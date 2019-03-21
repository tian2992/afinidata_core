from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from attributes.models import Attribute
from django.contrib import messages


class AttributesView(TemplateView):
    template_name = 'attributes/index.html'

    def get_context_data(self, **kwargs):
        attributes = Attribute.objects.all()
        return dict(attributes=attributes)


class NewAttributeView(CreateView):
    template_name = 'attributes/new.html'
    model = Attribute
    fields = ('name', 'type')

    def form_valid(self, form):
        form.save()
        return redirect('attributes:index')


class AttributeView(TemplateView):
    template_name = 'attributes/attribute.html'

    def get_context_data(self, **kwargs):
        attribute = get_object_or_404(Attribute, id=kwargs['id'])
        return dict(attribute=attribute)


class EditAttributeView(UpdateView):
    model = Attribute
    pk_url_kwarg = 'id'
    template_name = 'attributes/edit.html'
    fields = ('name', 'type')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Attribute has been updated')
        return redirect('attributes:index')
