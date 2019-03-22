from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from areas.models import Section, Area
from levels.models import Level
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages


class ListSectionView(ListView):
    template_name = 'sections/index.html'
    queryset = Section.objects.all()
    context_object_name = 'sections'


class SectionView(TemplateView):
    template_name = 'sections/section.html'

    def get_context_data(self, **kwargs):
        section = get_object_or_404(Section, id=kwargs['id'])
        return dict(section=section)


class CreateSectionView(CreateView):
    model = Section
    template_name = 'sections/new.html'
    fields = ('name', 'instance_name', 'area', 'level')

    def form_valid(self, form):
        section = form.save()
        messages.success(self.request, 'Section with name: "%s" has been created' % section.name)
        return redirect('sections:index')


class UpdateSectionView(UpdateView):
    template_name = 'sections/edit.html'
    model = Section
    fields = ('name', 'instance_name', 'area', 'level')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        section = form.save()
        messages.success(self.request, 'Level with name %s has been updated' % section.name)
        return redirect('sections:index')
