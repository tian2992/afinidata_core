from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from instances.forms import InstanceModelForm


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
