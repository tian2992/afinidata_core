from messenger_users.models import Child, User, ChildData
from django.contrib.auth.mixins import LoginRequiredMixin
from instances.models import Instance, Response
from django.views.generic import TemplateView
from milestones.models import Milestone
from entities.models import Entity
from posts.models import Interaction
from bots.models import Bot


class GetChildrenView(LoginRequiredMixin, TemplateView):
    template_name = 'utilities/get_children.html'

    def get_context_data(self, **kwargs):
        context = super(GetChildrenView, self).get_context_data()
        context['children'] = Child.objects.all()
        entity = Entity.objects.get(name='Niño')
        bot = Bot.objects.get(name='Afinibot')
        context['created'] = 0
        for child in context['children']:
            if Instance.objects.filter(user_id=child.parent_user_id).count() == 0:
                instance = Instance.objects.create(bot=bot, entity=entity, user_id=child.parent_user_id,
                                                   name=child.name)
                context['created'] = context['created'] + 1
                print(instance)
                print(context['created'])
        return context


class GetChildrenMilestonesView(LoginRequiredMixin, TemplateView):
    template_name = 'utilities/get_children_milestones.html'

    def get_context_data(self, **kwargs):
        context = super(GetChildrenMilestonesView, self).get_context_data()
        context['created'] = 0
        for instance in Instance.objects.all():
            parent = User.objects.get(id=instance.user_id)
            child_data = ChildData.objects\
                .filter(child__parent_user=parent,
                        data_key__in=[milestone.second_code for milestone in Milestone.objects.all()],
                        data_value__in=['Completado', 'done', 'Si lo hace'])
            parent_data = parent.userdata_set.filter(
                data_key__in=[milestone.second_code for milestone in Milestone.objects.all()],
                data_value__in=['Completado', 'done', 'Si lo hace'])

            negative_child_data = ChildData.objects\
                .filter(child__parent_user=parent,
                        data_key__in=[milestone.second_code for milestone in Milestone.objects.all()],
                        data_value__in=['Todavía no'])

            negative_parent_data = parent.userdata_set.filter(
                data_key__in=[milestone.second_code for milestone in Milestone.objects.all()],
                data_value__in=['Todavía no'])

            if negative_child_data.count() > 0:
                for data in negative_child_data:
                    response = Response.objects.create(instance=instance,
                                                       milestone=Milestone.objects.get(second_code=data.data_key),
                                                       response='failed',
                                                       created_at=data.timestamp)
                    print(response)
                    context['created'] = context['created'] + 1

            if negative_parent_data.count() > 0:
                for data in negative_parent_data:
                    response = Response.objects.create(instance=instance,
                                                       milestone=Milestone.objects.get(second_code=data.data_key),
                                                       response='failed',
                                                       created_at=data.created)
                    print(response)
                    context['created'] = context['created'] + 1

            if parent_data.count() > 0:
                for data in parent_data:
                    if instance.response_set.filter(milestone__second_code=data.data_key, response='done').count() < 1:
                        response = Response.objects.create(instance=instance,
                                                           milestone=Milestone.objects.get(second_code=data.data_key),
                                                           response='done',
                                                           created_at=data.created)
                        print(instance.pk, response.milestone, response.response)
                        context['created'] = context['created'] + 1

            if child_data.count() > 0:
                print(instance.pk)
                for data in child_data:
                    if instance.response_set.filter(milestone__second_code=data.data_key, response='done').count() < 1:
                        response = Response.objects.create(instance=instance,
                                                           milestone=Milestone.objects.get(second_code=data.data_key),
                                                           response='done',
                                                           created_at=data.timestamp)
                        print(instance.pk, response.milestone, response.response)
                        context['created'] = context['created'] + 1

        return context


class GetChildrenInteractionsView(LoginRequiredMixin, TemplateView):
    template_name = 'utilities/get_children_interactions.html'

    def get_context_data(self, **kwargs):
        context = super(GetChildrenInteractionsView, self).get_context_data()
        for instance in Instance.objects.all():
            print(instance.user_id)
        return context
