from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from instances.models import Instance,  Score, ScoreTracking, AttributeValue
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from instances.forms import ScoreModelForm, ScoreTrackingModelForm, InstanceAttributeValueForm
from django.contrib import messages


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
    fields = ('entity', 'bot', 'name', 'bot_user_id')

    def form_valid(self, form):
        form.save()
        return redirect('instances:index')


class EditInstanceView(UpdateView):
    model = Instance
    fields = ('entity', 'bot', 'name', 'bot_user_id')
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


class AddAttributeToInstance(View):

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        queryset = instance.entity.attributes.all().difference(instance.attributes.all())
        form = InstanceAttributeValueForm(request.GET or None, queryset=queryset)
        return render(self.request, 'instances/add_attribute_value.html', dict(form=form))

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        attribute = get_object_or_404(instance.entity.attributes, id=request.POST['attribute'])
        if attribute:
            queryset = instance.entity.attributes.filter(id=request.POST['attribute'])
        form = InstanceAttributeValueForm(request.POST, queryset=queryset)

        if form.is_valid():
            attr = AttributeValue.objects.create(instance=instance, attribute=attribute, value=request.POST['value'])
            print(attr)
            messages.success(request, 'Attribute has been added to instance')
            return redirect('instances:instance', id=kwargs['id'])

        return JsonResponse(dict(hello='world'))


@csrf_exempt
def score(request):

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
        return JsonResponse(dict(status='founded', data=dict(
            instances=[]
        )))
    else:
        instances_to_return = []
        for instance in instances:
            instances_to_return.append(dict(id=instance.pk, name=instance.name))

        return JsonResponse(dict(status='founded', data=dict(instances=instances_to_return)))
