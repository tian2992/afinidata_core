from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, UpdateView
from areas.forms import AreaFormModel, MilestonesByAreaForm
from areas.models import Area
from milestones.models import Milestone, Step
import random
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'areas/index.html'

    def get_context_data(self, **kwargs):

        areas = Area.objects.all()

        return dict(areas=areas)


class EditAreaView(UpdateView):
    model = Area
    fields = ('name', 'description')
    template_name = 'areas/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'area'

    def form_valid(self, form):
        area = form.save(commit=False)
        area.save()
        messages.success(self.request, 'Area with name: "%s" has been updated.' % area.name)
        return redirect('areas:area', id=area.pk)


class AreaView(TemplateView):
    template_name = 'areas/area.html'

    def get_context_data(self, **kwargs):
        area = get_object_or_404(Area, pk=kwargs['id'])

        return dict(area=area)


class NewAreaView(View):
    template_name = 'areas/new.html'

    def post(self, request, *args, **kwargs):
        form = AreaFormModel(request.POST)

        if form.is_valid():
            area = form.save()
            messages.success(request, 'Area with name: "%s" has been created' % area.name)
            return redirect('areas:index')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = AreaFormModel(request.POST or None)

        return render(request, self.template_name, {'form': form})


@csrf_exempt
def milestones_by_area(request, id):
    area = get_object_or_404(Area, pk=id)
    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='Invalid method'))

    form = MilestonesByAreaForm(request.GET)

    if form.is_valid():
        step = get_object_or_404(Step, step=request.GET['step'])
        step_value = step.value + float(request.GET['value']) \
            if request.GET['type'] == 'increment' \
            else float(request.GET['value']) - step.value
        step_limit = step_value + 1
        milestones = get_list_or_404(Milestone, value__gte=step_value, area=area, value__lte=step_limit)
        limit = random.randrange(len(milestones))
        milestone = milestones[limit]
        return JsonResponse(dict(
            data=dict(
                milestone=dict(
                    id=milestone.pk,
                    name=milestone.name,
                    area=milestone.area.pk
                )
            ),
            status='founded'
        ))
    else:
        print('invalid')
    return JsonResponse(dict(status='error', error='invalid params'))
