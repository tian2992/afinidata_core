from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from bots.models import Bot
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    model = Bot
    paginate_by = 10
    context_object_name = 'bots'
    login_url = reverse_lazy('pages:login')


class BotView(LoginRequiredMixin, DetailView):
    model = Bot
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('pages:login')


class CreateBotView(LoginRequiredMixin, CreateView):
    model = Bot
    fields = ('name', 'description')
    login_url = reverse_lazy('pages:login')

    def get_context_data(self, **kwargs):
        c = super(CreateBotView, self).get_context_data()
        c['action'] = 'Create'
        return c

    def get_success_url(self):
        messages.success(self.request, 'Bot with name: %s has been created.' % self.object.name)
        return reverse_lazy('bots:bot', kwargs={'id': self.object.pk})


class UpdateBotView(LoginRequiredMixin, UpdateView):
    model = Bot
    fields = ('name', 'description')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('pages:login')

    def get_context_data(self, **kwargs):
        c = super(UpdateBotView, self).get_context_data()
        c['action'] = 'Edit'
        return c

    def get_success_url(self):
        messages.success(self.request, 'Bot with name: %s has been updated.' % self.object.name)
        return reverse_lazy('bots:bot', kwargs={'id': self.object.pk})


class DeleteBotView(LoginRequiredMixin, DeleteView):
    model = Bot
    template_name = 'bots/delete.html'
    pk_url_kwarg = 'id'
    context_object_name = 'bot'
    login_url = reverse_lazy('pages:login')
    success_url = reverse_lazy('bots:index')
