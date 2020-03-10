from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from attributes.models import Attribute
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class AttributesView(LoginRequiredMixin, ListView):
    template_name = 'attributes/index.html'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    model = Attribute
    context_object_name = 'attributes'
    paginate_by = 10


class NewAttributeView(LoginRequiredMixin, CreateView):
    model = Attribute
    fields = ('name', 'type')
    login_url = reverse_lazy('pages:login')

    def get_success_url(self):
        messages.success(self.request, 'Attribute with name: %s has been created.' % self.object.name)
        return reverse_lazy('attributes:attribute', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        c = super(NewAttributeView, self).get_context_data()
        c['action'] = 'Create'
        return c


class AttributeView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('pages:login')
    pk_url_kwarg = 'id'
    model = Attribute


class EditAttributeView(LoginRequiredMixin, UpdateView):
    model = Attribute
    pk_url_kwarg = 'id'
    template_name = 'attributes/edit.html'
    fields = ('name', 'type')
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Attribute has been updated')
        return redirect('attributes:index')


class DeleteAttributeView(LoginRequiredMixin, DeleteView):
    model = Attribute
    template_name = 'attributes/delete.html'
    pk_url_kwarg = 'id'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('attributes:index')
