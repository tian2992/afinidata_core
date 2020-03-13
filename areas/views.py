from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import UpdateView, ListView, DetailView, DeleteView, CreateView
from areas.forms import  MilestonesByAreaForm
from areas.models import Area
from milestones.models import Milestone, Step
import random
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'areas/index.html'
    model = Area
    paginate_by = 10
    context_object_name = 'areas'
    login_url = reverse_lazy('pages:login')
    redirect_field_name = 'next'


class EditAreaView(LoginRequiredMixin, UpdateView):
    model = Area
    fields = ('name', 'description')
    template_name = 'areas/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'area'
    login_url = reverse_lazy('pages:login')
    redirect_field_name = 'next'

    def form_valid(self, form):
        area = form.save()
        messages.success(self.request, 'Area with name: "%s" has been updated.' % area.name)
        return redirect('areas:area', id=area.pk)


class AreaView(LoginRequiredMixin, DetailView):
    model = Area
    pk_url_kwarg = 'id'
    context_object_name = 'area'
    login_url = reverse_lazy('pages:login')
    redirect_field_name = 'next'


class NewAreaView(LoginRequiredMixin, CreateView):
    template_name = 'areas/new.html'
    model = Area
    fields = ('name', 'description')
    login_url = reverse_lazy('pages:login')
    redirect_field_name = 'next'

    def form_valid(self, form):
        area = form.save()
        messages.success(self.request, 'Area with name: %s has been created.' % area.name)
        return redirect('areas:index')


class DeleteAreaView(LoginRequiredMixin, DeleteView):
    template_name = 'areas/delete.html'
    model = Area
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('pages:login')
    redirect_field_name = 'next'
    success_url = reverse_lazy('areas:index')


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
