from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView
from milestones.forms import MilestoneFormModel, ResponseMilestoneForm
from milestones.models import Milestone, Step
from instances.models import Instance, Response, Score
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = 'milestones/index.html'

    def get_context_data(self, **kwargs):
        milestones = Milestone.objects.all()

        return dict(milestones=milestones)


class MilestoneView(TemplateView):
    template_name = 'milestones/milestone.html'

    def get_context_data(self, **kwargs):
        milestone = get_object_or_404(Milestone, pk=kwargs['id'])

        return dict(milestone=milestone)


class EditMilestoneView(UpdateView):
    model = Milestone
    fields = ('name', 'code', 'area', 'value', 'secondary_value', 'description')
    template_name = 'milestones/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'milestone'

    def form_valid(self, form):
        milestone = form.save(commit=False)
        milestone.save()
        return redirect('milestones:milestone', id=milestone.pk)


class NewMilestoneView(View):
    template_name = 'milestones/new.html'

    def post(self, request, *args, **kwargs):
        form = MilestoneFormModel(request.POST)

        if form.is_valid():
            form.save()
            return redirect('milestones:index')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = MilestoneFormModel(request.POST or None)

        return render(request, self.template_name, {'form': form})


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
