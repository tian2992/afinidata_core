from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from forms.models import Form, Validation
from django.contrib import messages
from django.http import JsonResponse
from forms.forms import FormAttributeForm


class HomeView(TemplateView):
    template_name = 'forms/index.html'

    def get_context_data(self, **kwargs):
        forms = Form.objects.all()
        return dict(forms=forms)


class FormView(TemplateView):
    template_name = 'forms/form.html'

    def get_context_data(self, **kwargs):
        form = get_object_or_404(Form, id=kwargs['id'])
        return dict(form=form)


class CreateFormView(CreateView):
    template_name = 'forms/new.html'
    model = Form
    fields = ('name', 'entity')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Form has been created')
        return redirect('forms:index')


class UpdateFormView(UpdateView):
    template_name = 'forms/edit.html'
    model = Form
    fields = ('name', 'entity')
    pk_url_kwarg = 'id'
    context_object_name = 'form'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Form has been updated')
        return redirect('forms:index')


class AddAttributeToForm(View):

    def get(self, request, *args, **kwargs):
        view_form = get_object_or_404(Form, id=kwargs['id'])
        form = FormAttributeForm(request.POST or None, form=view_form)
        return render(request, 'forms/add_attribute.html', dict(form=form))

    def post(self, request, *args, **kwargs):
        view_form = get_object_or_404(Form, id=kwargs['id'])
        form = FormAttributeForm(request.POST, form=view_form)

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


class ValidationView(TemplateView):

    template_name = 'forms/validation.html'

    def get_context_data(self, **kwargs):
        validation = get_object_or_404(Validation, id=kwargs['id'])
        return dict(validation=validation)


class ValidationEditView(UpdateView):
    model = Validation
    template_name = 'forms/validation-edit.html'
    fields = ('min', 'max', 'distinct_of', 'match_with')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        validation = form.save()
        messages.success(self.request, 'Validation has been updated')
        return redirect('forms:validation', id=validation.pk)
