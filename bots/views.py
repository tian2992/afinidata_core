from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from bots.models import Bot


class HomeView(TemplateView):
    template_name = 'bots/index.html'

    def get_context_data(self, **kwargs):
        bots = Bot.objects.all()
        return dict(bots=bots)


class BotView(TemplateView):
    template_name = 'bots/bot.html'

    def get_context_data(self, **kwargs):
        bot = get_object_or_404(Bot, pk=kwargs['id'])
        return dict(bot=bot)


class CreateBotView(CreateView):
    model = Bot
    template_name = 'bots/new.html'
    fields = ('name',)

    def form_valid(self, form):
        form.save()
        return redirect('bots:index')


class UpdateBotView(UpdateView):
    model = Bot
    template_name = 'bots/edit.html'
    fields = ('name',)
    pk_url_kwarg = 'id'
    context_object_name = 'bot'

    def form_valid(self, form):
        bot = form.save()
        return redirect('bots:edit', bot.pk)


class DeleteBotView(DeleteView):
    model = Bot
    template_name = 'bots/delete.html'
    pk_url_kwarg = 'id'
    context_object_name = 'bot'

    success_url = reverse_lazy('bots:index')
