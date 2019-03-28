from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from instances.models import Instance,  Score, ScoreTracking, AttributeValue, InstanceSection, Response
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from instances.forms import ScoreModelForm, ScoreTrackingModelForm, InstanceAttributeValueForm, \
     InstanceSectionForm
from django.contrib import messages
from areas.models import Area, Section
from levels.models import Level
from datetime import datetime, timedelta
from milestones.models import Milestone
from attributes.models import Attribute


class HomeView(TemplateView):
    template_name = 'instances/index.html'

    def get_context_data(self, **kwargs):
        instances = Instance.objects.all()
        return dict(instances=instances)


class InstanceView(TemplateView):
    template_name = 'instances/instance.html'

    def get_context_data(self, **kwargs):
        instance = get_object_or_404(Instance, pk=kwargs['id'])

        return dict(instance=instance)


class NewInstanceView(CreateView):
    model = Instance
    template_name = 'instances/new.html'
    fields = ('entity', 'bot', 'name', 'bot_user_id')

    def form_valid(self, form):
        form.save()
        return redirect('instances:index')


class EditInstanceView(UpdateView):
    model = Instance
    fields = ('entity', 'bot', 'name', 'bot_user_id')
    template_name = 'instances/edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'instance'

    def form_valid(self, form):
        entity = form.save()
        return redirect('instances:edit', entity.pk)


class DeleteInstanceView(DeleteView):
    model = Instance
    template_name = 'instances/delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('instances:index')


class AddAttributeToInstance(View):

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        queryset = instance.entity.attributes.all().difference(instance.attributes.all())
        form = InstanceAttributeValueForm(request.GET or None, queryset=queryset)
        return render(self.request, 'instances/add_attribute_value.html', dict(form=form))

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        attribute = get_object_or_404(instance.entity.attributes, id=request.POST['attribute'])
        if attribute:
            queryset = instance.entity.attributes.filter(id=request.POST['attribute'])
        form = InstanceAttributeValueForm(request.POST, queryset=queryset)

        if form.is_valid():
            attr = AttributeValue.objects.create(instance=instance, attribute=attribute, value=request.POST['value'])
            print(attr)
            messages.success(request, 'Attribute has been added to instance')
            return redirect('instances:instance', id=kwargs['id'])

        return JsonResponse(dict(hello='world'))


@csrf_exempt
def score(request):

    if request.method == 'POST':
        form = ScoreModelForm(request.POST)
        tracking_form = ScoreTrackingModelForm(request.POST)

        if form.is_valid():
            instance_score, response = Score.objects.get_or_create(
                area_id=request.POST['area'],
                instance_id=request.POST['instance']
            )
            instance_score.value = request.POST['value']
            instance_score.save()

        if tracking_form.is_valid():
            tracking_form.save()

            return JsonResponse(dict(status='done', data=dict(message='score has been created or updated')))
        else:
            return JsonResponse(dict(status='error', error='invalid params'))
    else:
        return JsonResponse(dict(status='error', error='invalid method'))


@csrf_exempt
def instances_by_user(request, id):

    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='invalid method'))

    instances = Instance.objects.filter(bot_user_id=id)

    if instances.count() <= 0:
        return JsonResponse(dict(status='founded', data=dict(
            instances=[]
        )))
    else:
        instances_to_return = []
        for instance in instances:
            instances_to_return.append(dict(id=instance.pk, name=instance.name))

        return JsonResponse(dict(status='founded', data=dict(instances=instances_to_return)))


class InstanceSectionView(View):

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        queryset = Area.objects.all().difference(instance.areas.all())
        form = InstanceSectionForm(None, queryset=queryset)
        return render(request, 'instances/section_to_instance.html', dict(form=form))

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        queryset = Area.objects.filter(id=request.POST['area'])
        form = InstanceSectionForm(request.POST, queryset=queryset)

        if form.is_valid():
            level = Level.objects.get(max__gte=int(request.POST['value_to_init']),
                                      min__lte=int(request.POST['value_to_init']))
            area = get_object_or_404(Area, id=request.POST['area'])
            section = get_object_or_404(Section, level=level, area=area)
            instance_section = InstanceSection.objects.create(value_to_init=request.POST['value_to_init'],
                                                              section=section,
                                                              instance=instance,
                                                              area=area)
            print(instance_section)
            messages.success(request, 'Instance has been added to section "%s".' % section.name)
            return redirect('instances:instance', id=instance.pk)


class Evaluator(View):

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Instance, id=kwargs['id'])
        area = get_object_or_404(Area, id=int(request.GET['area']))
        section = get_object_or_404(Section, instance=instance, area=area)
        last_milestones = Milestone.objects.filter(area=area,
                                                   value__gte=section.level.min,
                                                   value__lte=section.level.max).order_by('-value', '-created_at')[:3]

        last_milestones_ids = [milestone.pk for milestone in last_milestones]

        instance_responses = Response.objects.filter(instance=instance,
                                                     created_at__gte=(datetime.now() - timedelta(days=30)))

        search_responses = instance_responses.filter(milestone_id__in=last_milestones_ids)\
            .order_by('-milestone_id', '-id')
        if search_responses.filter(milestone_id=last_milestones_ids[0]).count() > 0:
            print(search_responses.filter(milestone_id=last_milestones_ids[0]))
            if search_responses.count() >= 3:
                instance_has_up = True

                for milestone in last_milestones:
                    milestone_init = False
                    responses = search_responses.filter(milestone__id=milestone.pk)
                    for response in responses:
                        if response.response == 'true':
                            milestone_init = True
                    print(milestone.pk, milestone.name, milestone_init, responses.count())

                    if not milestone_init:
                        instance_has_up = False

                if instance_has_up:
                    attribute_name = "%s__has__up" % area.name
                    attribute = Attribute.objects.update_or_create(name=attribute_name,
                                                                   defaults=dict(name=attribute_name, type='boolean'))
                    attribute = attribute[0]
                    instance.entity.attributes.add(attribute)
                    attribute_value = AttributeValue.objects.update_or_create(instance=instance,
                                                                              attribute=attribute,
                                                                              defaults=dict(value=True))
                    return JsonResponse(dict(status='done', data=dict(message='Instance must be up section.',
                                                                      up=True, down=False)))

                if not instance_has_up:
                    return JsonResponse(dict(status='done', data=dict(message='Instance not change section.',
                                                                      up=False,
                                                                      down=False)))
            else:
                return JsonResponse(dict(status='done', data=dict(message='Instance not change section.',
                                                                  up=False, down=False)))

        first_milestones = Milestone.objects.filter(area=area,
                                                    value__gte=section.level.min,
                                                    value__lte=section.level.max).order_by('value', 'created_at')[:3]
        first_milestones_ids = [milestone.pk for milestone in first_milestones]
        search_responses = instance_responses.filter(milestone_id__in=first_milestones_ids)\
            .order_by('milestone_id', 'id')

        if search_responses.filter(milestone_id=first_milestones_ids[0], response='false').count() > 0:
            instance_has_down = True
            index = 0
            while instance_has_down:
                if search_responses[index].response == 'true':
                    instance_has_down = False
                index = index + 1
                if index == search_responses.count():
                    break

            if instance_has_down:
                change_level_number = section.level.min - 1
                try:
                    new_section = Section.objects.get(level__max__gte=change_level_number,
                                                      level__min__lte=change_level_number)
                    attribute = Attribute.objects.update_or_create(name="%s__has__descended" % area.name,
                                                                   defaults=dict(type='string'))
                    attribute = attribute[0]
                    instance.entity.attributes.add(attribute)
                    instance.attributevalue_set.create(attribute=attribute,
                                                       value='instance: %s descended of %s (%s) to %s (%s). date: %s' %
                                                             (instance.name, section.name, section.pk, new_section.name,
                                                              new_section.pk, datetime.now()))
                    actual_section_to_instance = InstanceSection.objects.get(instance=instance,
                                                                             section=section)
                    print(actual_section_to_instance)
                    actual_section_to_instance.delete()
                    new_section_to_instance = InstanceSection.objects.create(instance=instance, section=new_section,
                                                                             area=area,
                                                                             value_to_init=change_level_number)
                    print(new_section_to_instance)
                    return JsonResponse(dict(status='done', data=dict(message='Instance down section',
                                                                      up=False, down=True)))
                except Exception as e:
                    return JsonResponse(dict(status='error', error='%s' % str(e)))

        return JsonResponse(dict(status='done', data=dict(message='Instance not change section',
                                                          up=False, down=False)))
