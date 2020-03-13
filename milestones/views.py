from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from milestones.models import Milestone
from django.urls import reverse_lazy
from django.contrib import messages


class HomeView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    context_object_name = 'milestones'
    paginate_by = 50


class MilestoneView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    pk_url_kwarg = 'id'


class EditMilestoneView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    fields = ('name', 'code', 'second_code', 'area', 'value', 'secondary_value', 'description')
    pk_url_kwarg = 'id'
    context_object_name = 'milestone'

    def get_success_url(self):
        messages.success(self.request, 'Milestone with Code: "%s" has been updated.' % self.object.code)
        return reverse_lazy('milestones:milestone', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        c = super(EditMilestoneView, self).get_context_data()
        c['action'] = 'Edit'
        return c


class NewMilestoneView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    fields = ('name', 'code', 'second_code', 'area', 'value', 'secondary_value', 'description')

    def get_success_url(self):
        messages.success(self.request, 'Milestone with Code: "%s" has been created.' % self.object.code)
        return reverse_lazy('milestones:milestone', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        c = super(NewMilestoneView, self).get_context_data()
        c['action'] = 'Create'
        return c
