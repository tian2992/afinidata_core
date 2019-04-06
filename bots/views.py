from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from bots.models import Bot
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'bots/index.html'
    model = Bot
    paginate_by = 10
    context_object_name = 'bots'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'


class BotView(LoginRequiredMixin, DetailView):
    template_name = 'bots/bot.html'
    model = Bot
    pk_url_kwarg = 'id'
    context_object_name = 'bot'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'


class CreateBotView(LoginRequiredMixin, CreateView):
    model = Bot
    template_name = 'bots/new.html'
    fields = ('name',)
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        bot = form.save()
        messages.success(self.request, 'Bot with name: %s has been created.' % bot.name)
        return redirect('bots:index')


class UpdateBotView(LoginRequiredMixin, UpdateView):
    model = Bot
    template_name = 'bots/edit.html'
    fields = ('name',)
    pk_url_kwarg = 'id'
    context_object_name = 'bot'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        bot = form.save()
        messages.success(self.request, 'Bot with name: %s has been updated.' % bot.name)
        return redirect('bots:edit', bot.pk)


class DeleteBotView(LoginRequiredMixin, DeleteView):
    model = Bot
    template_name = 'bots/delete.html'
    pk_url_kwarg = 'id'
    context_object_name = 'bot'
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    success_url = reverse_lazy('bots:index')
