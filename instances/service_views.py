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
