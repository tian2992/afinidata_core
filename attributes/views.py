from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from attributes.models import Attribute


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
