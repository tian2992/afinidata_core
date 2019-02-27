from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

@csrf_exempt
def get_user_instances(request, id):

    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='Invalid method'))

    request_domain = settings.DOMAIN_URL + '/instances/by_bot_user/' + str(id)
    r = requests.get(request_domain)
    data = r.json()
    if data['status'] != 'error':
        attributes = dict()
        instances = data['data']['instances']

        if len(instances) > 0:
            for index, instance in enumerate(instances):
                attributes['instance__' + str(index + 1)] = instance['id']
                attributes['instance__' + str(index + 1) + '__name'] = instance['name']

        return JsonResponse(dict(
            set_attributes=attributes,
            messages=[]
        ))
    else:
        return JsonResponse(dict(status='error', error=str(data['error'])))
