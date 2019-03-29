from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from areas.forms import MilestonesByAreaForm
from milestones.forms import ResponseMilestoneForm
from instances.forms import ScoreModelForm, InstanceModelForm
from instances.models import Instance, InstanceSection
from areas.models import Area, Section
from chatfuel.forms import SetSectionToInstance
from milestones.models import Milestone
from django.views.generic import View
import requests


@csrf_exempt
def get_user_instances(request, id):

    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='Invalid method'))

    response_label = 'Choice Instance: '

    try:
        response_label = request.GET['label']
        print(response_label)
    except Exception as e:
        pass

    request_uri = settings.DOMAIN_URL + '/instances/by_bot_user/' + str(id)
    r = requests.get(request_uri)
    response = r.json()
    if response['status'] != 'error':
        attributes = dict()
        instances = response['data']['instances']
        replies = []

        if len(instances) > 0:
            for index, instance in enumerate(instances):
                attributes['instance__' + str(index + 1)] = instance['id']
                attributes['instance__' + str(index + 1) + '__name'] = instance['name']

                replies.append(dict(
                    title=instance['name'],
                    set_attributes=dict(
                        instance=instance['id'],
                        instance_name=instance['name']
                    )
                ))

        return JsonResponse(dict(
            set_attributes=attributes,
            messages=[
                dict(
                    text=response_label,
                    quick_replies=replies
                )
            ]
        ))
    else:
        return JsonResponse(dict(status='error', error=str(response['error'])))


@csrf_exempt
def create_instance(request):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error="Invalid method."))

    form = InstanceModelForm(request.POST)

    if not form.is_valid():
        return JsonResponse(dict(status="error", error="Invalid params."))

    new_instance = form.save()

    return JsonResponse(dict(
        set_attributes=dict(
            instance=new_instance.pk,
            instance_name=new_instance.name
        ),
        messages=[]
    ))


@csrf_exempt
def milestone_by_area(request, id):

    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='Invalid method'))

    try:
        instance = Instance.objects.get(id=id)
        area = Area.objects.get(id=request.GET['area'])
    except Exception as e:
        return JsonResponse(dict(status='error', error='Invalid params. %s' % e))

    request_uri = settings.DOMAIN_URL + '/instances/' + str(id) + '/milestone/'

    if area and instance:
        print(request.GET)
        r = requests.get(request_uri, params=request.GET)
        response = r.json()
        print(response)
        if(response['status']) == 'error':
            return JsonResponse(dict(status='error', error=response['error']))

        if not response['data']['milestone']:
            return JsonResponse(dict(
                set_attributes=dict(
                    milestone_id=None,
                    milestone_name=None,
                    core_message=response['data']['message']
                ),
                messages=[]
            ))

        return JsonResponse(dict(
            set_attributes=dict(
                milestone=response['data']['milestone']['id'],
                milestone_name=response['data']['milestone']['name']
            ),
            messages=[]
        ))
        
    else:
        return JsonResponse(dict(status='error', error='Invalid params'))


@csrf_exempt
def response_milestone_for_instance(request, milestone_id):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error='Invalid method'))
    form = ResponseMilestoneForm(request.POST)

    if form.is_valid():
        request_uri = settings.DOMAIN_URL + '/milestones/' + str(milestone_id) + '/response/'
        r = requests.post(request_uri, request.POST)
        response = r.json()

        if response['status'] == 'error':
            return JsonResponse(dict(status='error', error=response['error']))

        instance = Instance.objects.get(id=request.POST['instance'])
        milestone = Milestone.objects.get(id=milestone_id)

        set_attributes = dict(
            core_message='Response for instance: %s to milestone: "%s" is %s' % (
                instance.name,
                milestone.name,
                request.POST['response']
            )
        )
        return JsonResponse(dict(set_attributes=set_attributes, messages=[]))
    else:
        return JsonResponse(dict(status='error', error='Invalid params'))


@csrf_exempt
def set_area_value_to_instance(request):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error='Invalid method'))

    form = ScoreModelForm(request.POST)

    if not form.is_valid():
        return JsonResponse(dict(status='error', error='Invalid params'))

    request_uri = settings.DOMAIN_URL + '/instances/score/'
    r = requests.post(request_uri, request.POST)
    response = r.json()

    return JsonResponse(response)


@csrf_exempt
def set_sections_by_value(request):
    if request.method == 'GET':
        return JsonResponse(dict(status='error', error='Invalid method'))

    form = SetSectionToInstance(request.POST)
    if not form.is_valid():
        return JsonResponse(dict(status='error', error='Invalid params.'))

    instance = get_object_or_404(Instance, id=request.POST['instance'])
    value = int(request.POST['value'])
    areas = Area.objects.all()
    areas_string = ''
    sections_string = ''
    for area in areas:
        section = None
        try:
            section = Section.objects.get(area=area, level__min__lte=value, level__max__gte=value)
            print(section)
        except Exception as e:
            print('error: ', str(e))
            pass
        if section:
            areas_string = areas_string + "%s, " % area.name
            sections_string = sections_string + "%s, " % section.name
            new_instance_section = InstanceSection.objects.update_or_create(instance=instance, area=area, defaults=dict(
                value_to_init=value,
                instance=instance,
                area=area,
                section=section
            ))
            print(new_instance_section)

    return JsonResponse(dict(set_attributes=dict(
        core_message='Instance has been added to sections %s to areas %s' % (sections_string, areas_string)
    ), messages=[]))


class Evaluator(View):

    def get(self, request):
        try:
            instance = Instance.objects.get(id=request.GET['instance'])
            area = Area.objects.get(id=request.GET['area'])
        except Exception as e:
            return JsonResponse(dict(status='error', error='Invalid params: %s' % e))

        request_uri = '%s/instances/%s/evaluator/?area=%s' % (settings.DOMAIN_URL, instance.pk, area.pk)
        r = requests.get(request_uri)
        response = r.json()
        print(response)
        return JsonResponse(dict(
            set_attributes=dict(
                instance_has_up=response['data']['up'],
                instance_has_down=response['data']['down'],
                core_message=response['data']['message']
            ),
            messages=[]
        ))


@csrf_exempt
def up_instance(request, id):
    if request.method == 'GET':
        return JsonResponse(dict(set_attributes=dict(core_message='Invalid method')), messages=[])
    try:
        area = request.POST['area']
    except Exception as e:
        return JsonResponse(dict(set_attributes=dict(core_message='Invalid params: %s' % e), messages=[]))

    request_uri = "%s/instances/%s/up/" % (settings.DOMAIN_URL, id)
    r = requests.post(request_uri, request.POST)
    response = r.json()
    if response['status'] == 'error':
        core_message = response['error']
    else:
        core_message = response['data']['message']
    return JsonResponse(dict(set_attributes=dict(core_message=core_message, up=None, down=None),
                             messages=[]))
