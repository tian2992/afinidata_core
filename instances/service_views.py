from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from instances.forms import InstanceModelForm
from instances.models import Instance, InstanceSection, Response
from milestones.models import Milestone
from datetime import datetime, timedelta


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
    responses = Response.objects.filter(instance=instance, created_at__gte=day)
    milestones_responses = set()
    for response in responses:
        milestones_responses.add(response.milestone.pk)
    milestones = Milestone.objects.filter(area=area,
                                          value__lte=level.max,
                                          value__gte=level.min)\
        .exclude(id__in=milestones_responses)\
        .order_by('value')

    try:
        milestone = milestones.first()
    except Exception as e:
        return JsonResponse(dict(status='error', error='%s' % str(e)))

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
