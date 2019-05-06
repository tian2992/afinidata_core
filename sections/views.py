from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from areas.models import Section, Area
from milestones.models import Milestone
from levels.models import Level
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class ListSectionView(LoginRequiredMixin, ListView):

    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'sections/index.html'
    queryset = Section.objects.all()
    context_object_name = 'sections'


class SectionView(LoginRequiredMixin, DetailView):
    template_name = 'sections/section.html'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    pk_url_kwarg = 'id'
    model = Section
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['milestones'] = Milestone.objects.filter(area=context['section'].area,
                                                         value__gte=context['section'].level.min,
                                                         value__lte=context['section'].level.max)
        return context


class CreateSectionView(LoginRequiredMixin, CreateView):
    model = Section
    template_name = 'sections/new.html'
    fields = ('name', 'instance_name', 'area', 'level')
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        section = form.save()
        messages.success(self.request, 'Section with name: "%s" has been created' % section.name)
        return redirect('sections:index')


class UpdateSectionView(LoginRequiredMixin, UpdateView):
    template_name = 'sections/edit.html'
    model = Section
    fields = ('name', 'instance_name', 'area', 'level')
    pk_url_kwarg = 'id'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        section = form.save()
        messages.success(self.request, 'Level with name %s has been updated' % section.name)
        return redirect('sections:index')
