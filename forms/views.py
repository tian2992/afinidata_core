from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView, ListView, DetailView
from forms.models import Form, Validation
from attributes.models import Attribute
from django.contrib import messages
from django.http import JsonResponse
from forms.forms import FormAttributeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'forms/index.html'
    model = Form
    context_object_name = 'forms'
    paginate_by = 20
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'


class FormView(LoginRequiredMixin, DetailView):
    template_name = 'forms/form.html'
    model = Form
    pk_url_kwarg = 'id'
    context_object_name = 'form'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'


class CreateFormView(LoginRequiredMixin, CreateView):
    template_name = 'forms/new.html'
    model = Form
    fields = ('name', 'entity')
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Form has been created')
        return redirect('forms:index')


class UpdateFormView(LoginRequiredMixin, UpdateView):
    template_name = 'forms/edit.html'
    model = Form
    fields = ('name', 'entity')
    pk_url_kwarg = 'id'
    context_object_name = 'form'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Form has been updated')
        return redirect('forms:index')


class AddAttributeToForm(LoginRequiredMixin, View):

    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        view_form = get_object_or_404(Form, id=kwargs['id'])
        queryset = view_form.entity.attributes.all().difference(view_form.attributes.all())
        form = FormAttributeForm(request.POST or None, queryset=queryset)
        return render(request, 'forms/add_attribute.html', dict(form=form))

    def post(self, request, *args, **kwargs):
        view_form = get_object_or_404(Form, id=kwargs['id'])
        queryset = Attribute.objects.filter(id=request.POST['attribute'])
        form = FormAttributeForm(request.POST, queryset=queryset)
        print(form)

        if form.is_valid():
            params = form.cleaned_data
            params['form'] = view_form
            validation = Validation.objects.create(**params)
            messages.success(request, 'Validation has been created')
            return redirect('forms:form', id=kwargs['id'])

        else:
            view_form = get_object_or_404(Form, id=kwargs['id'])
            form = FormAttributeForm(request.POST, form=view_form)
            return render(request, 'forms/add_attribute.html', dict(form=form))


class ValidationView(LoginRequiredMixin, DetailView):

    template_name = 'forms/validation.html'
    model = Validation
    pk_url_kwarg = 'id'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'


class ValidationEditView(LoginRequiredMixin, UpdateView):
    model = Validation
    template_name = 'forms/validation-edit.html'
    fields = ('min', 'max', 'distinct_of', 'match_with')
    pk_url_kwarg = 'id'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        validation = form.save()
        messages.success(self.request, 'Validation has been updated')
        return redirect('forms:validation', id=validation.pk)
