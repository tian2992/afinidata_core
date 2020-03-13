from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView, CreateView
from milestones.forms import MilestoneFormModel, ResponseMilestoneForm
from milestones.models import Milestone, Step
from instances.models import Instance, Response, Score
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


class HomeView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    context_object_name = 'milestones'
    paginate_by = 50


class MilestoneView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('pages:login')
    template_name = 'milestones/milestone.html'

    def get_context_data(self, **kwargs):
        milestone = get_object_or_404(Milestone, pk=kwargs['id'])

        return dict(milestone=milestone)


class EditMilestoneView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    fields = ('name', 'code', 'second_code', 'area', 'value', 'secondary_value', 'description')
    pk_url_kwarg = 'id'
    context_object_name = 'milestone'

    def get_success_url(self):
        messages.success(self.request, 'Milestone with Code: "%s" has been updated.' % self.object.code)
        return reverse_lazy('milestones:milestone', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        c = super(EditMilestoneView, self).get_context_data()
        c['action'] = 'Edit'
        return c


class NewMilestoneView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('pages:login')
    model = Milestone
    fields = ('name', 'code', 'second_code', 'area', 'value', 'secondary_value', 'description')

    def get_success_url(self):
        messages.success(self.request, 'Milestone with Code: "%s" has been created.' % self.object.code)
        return reverse_lazy('milestones:milestone', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        c = super(NewMilestoneView, self).get_context_data()
        c['action'] = 'Create'
        return c


@csrf_exempt
def response_instance_to_milestone(request, id):

    if request.method == 'GET':
        return JsonResponse(dict(status='error', error='invalid params'))

    print(request.POST)

    milestone = get_object_or_404(Milestone, pk=id)

    form = ResponseMilestoneForm(request.POST)

    if form.is_valid():
        print('valid')
        instance = Instance.objects.get(id=request.POST['instance'])
        response = request.POST['response']

        if response == 'true':
            old_score = None
            new_value = milestone.value
            try:
                old_score = Score.objects.get(instance=instance, area=milestone.area)
                if old_score.value > milestone.value:
                    new_value = old_score.value
            except Exception as e:
                print(e)
                pass
            score = Score.objects.update_or_create(instance=instance, area=milestone.area, defaults=dict(
                instance=instance,
                area=milestone.area,
                value=new_value
            ))
            print(score)

        new_response = Response.objects.create(milestone=milestone, instance=instance, response=response)
        print(new_response)
        return JsonResponse(dict(
            status='finished',
            data=dict(
                area=milestone.area.pk,
                instance=instance.pk
            )
        ))

    else:
        return JsonResponse(dict(status='error', error='invalid params'))
