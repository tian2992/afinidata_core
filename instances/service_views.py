from instances.models import Instance, InstanceSection, Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from instances.forms import InstanceModelForm
from django.views.generic import CreateView
from datetime import datetime, timedelta
from milestones.models import Milestone
from instances import models


@csrf_exempt
def create_user(request):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error='Invalid method.'))

    form = InstanceModelForm(request.POST)

    if not form.is_valid():
        return JsonResponse(dict(status='error', error='Invalid params.'))

    instance = form.save()
    return JsonResponse(dict(
        status='done',
        data=dict(
            instance=dict(
                id=instance.pk,
                name=instance.name
            )
        )
    ))


@csrf_exempt
def milestone_by_area(request, id):

    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='Invalid method.'))

    try:
        area = request.GET['area']
        instance = Instance.objects.get(id=id)
        section = instance.sections.get(area=area)
        level = section.level
    except Exception as e:
        return JsonResponse(dict(status='error', error='Invalid params: %s' % str(e)))

    day = datetime.now() - timedelta(days=7)
    old_responses_day = datetime.now() - timedelta(days=90)
    responses = Response.objects.filter(instance=instance, created_at__gte=day)
    other_responses = Response.objects.filter(instance=instance, created_at__gte=old_responses_day, response='true')
    milestones_responses = set()
    for response in responses:
        print(response.created_at, response.response, response.milestone.name, response.milestone.pk)
        milestones_responses.add(response.milestone.pk)
    for response in other_responses:
        milestones_responses.add(response.milestone.pk)
    print('milestones responses: ', milestones_responses)
    milestones = Milestone.objects.filter(area=area,
                                          value__lte=level.max,
                                          value__gte=level.min)\
        .exclude(id__in=milestones_responses)\
        .order_by('value', 'created_at')

    if milestones.count() <= 0:
        return JsonResponse(dict(status='done', data=dict(
            milestone=None,
            message='Not milestones for this instance'
        )))

    milestone = milestones.first()

    response = dict(
        status='done',
        data=dict(
            milestone=dict(
                id=milestone.pk,
                name=milestone.name
            )
        )
    )
    return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class CreateInstanceAttributeView(CreateView):
    model = models.AttributeValue
    fields = ('attribute', 'value')

    def get_form(self, form_class=None):
        form = super(CreateInstanceAttributeView, self).get_form(form_class=None)
        instance = get_object_or_404(Instance, id=self.kwargs['instance_id'])
        form.fields['attribute'].queryset = instance.entity.attributes.all()
        form.fields['attribute'].to_field_name = 'name'
        return form

    def form_valid(self, form):
        form.instance.instance = get_object_or_404(Instance, id=self.kwargs['instance_id'])
        instance_value = form.save()
        if instance_value:
            return JsonResponse(dict(set_attributes=dict(status='done', result_id=instance_value.pk,
                                                         result_message='id: %s attribute %s value: %s' % (
                                                             instance_value.pk, instance_value.attribute.name,
                                                             instance_value.value
                                                         ))))

        return JsonResponse(dict(set_attributes=dict(status='error', error_name='instance_attribute_error',
                                                     error='Invalid params'), messages=[]))

    def form_invalid(self, form):
        return JsonResponse(dict(set_attributes=dict(status='error', error_name='instance_attribute_error',
                                                     error='Invalid params'), messages=[]))

    def get(self, request, *args, **kwargs):
        raise Http404
