from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from instances.models import Instance
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from instances.forms import ScoreModelForm, ScoreTrackingModelForm
from instances.models import Score, ScoreTracking


class HomeView(TemplateView):
    template_name = 'instances/index.html'

    def get_context_data(self, **kwargs):
        instances = Instance.objects.all()
        return dict(instances=instances)


class InstanceView(TemplateView):
    template_name = 'instances/instance.html'

    def get_context_data(self, **kwargs):
        instance = get_object_or_404(Instance, pk=kwargs['id'])

        return dict(instance=instance)


class NewInstanceView(CreateView):
    model = Instance
    template_name = 'instances/new.html'
    fields = ('entity', 'bot', 'name')

    def form_valid(self, form):
        form.save()
        return redirect('instances:index')


class EditInstanceView(UpdateView):
    model = Instance
    fields = ('entity', 'bot', 'name')
    template_name = 'instances/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'instance'

    def form_valid(self, form):
        entity = form.save()
        return redirect('instances:edit', entity.pk)


class DeleteInstanceView(DeleteView):
    model = Instance
    template_name = 'instances/delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('instances:index')


@csrf_exempt
def score(request, id):

    if request.method == 'POST':
        form = ScoreModelForm(request.POST)
        tracking_form = ScoreTrackingModelForm(request.POST)

        if form.is_valid():
            instance_score, response = Score.objects.get_or_create(
                area_id=request.POST['area'],
                instance_id=request.POST['instance']
            )
            instance_score.value = request.POST['value']
            instance_score.save()

        if tracking_form.is_valid():
            tracking_form.save()

            return JsonResponse(dict(status='done', data=dict(message='score has been created or updated')))
        else:
            return JsonResponse(dict(status='error', error='invalid params'))
    else:
        return JsonResponse(dict(status='error', error='invalid method'))


@csrf_exempt
def instances_by_user(request, id):

    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='invalid method'))

    instances = Instance.objects.filter(bot_user_id=id)

    if instances.count() <= 0:
        return JsonResponse(dict(status='founded', data=[]))
    else:
        instances_to_return = []
        for instance in instances:
            instances_to_return.append(dict(id=instance.pk, name=instance.name))

        return JsonResponse(dict(status='founded', data=dict(instances=instances_to_return)))
