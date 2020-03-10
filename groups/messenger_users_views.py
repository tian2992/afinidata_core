from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, CreateView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.contrib import messages
from groups import models, forms


class AddMessengerUserView(PermissionRequiredMixin, CreateView):
    permission_required = 'posts.add_assignationmessengeruser'
    model = models.AssignationMessengerUser
    fields = ('messenger_user_id',)

    def get_context_data(self, **kwargs):
        c = super(AddMessengerUserView, self).get_context_data()
        c['action'] = 'Add'
        c['group'] = get_object_or_404(models.Group, id=self.kwargs['group_id'])
        return c

    def form_valid(self, form):
        form.instance.group = get_object_or_404(models.Group, id=self.kwargs['group_id'])
        return super(AddMessengerUserView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Messenger User: "%s %s" has been added to group.' %
                         (self.object.get_messenger_user().get_first_name(),
                          self.object.get_messenger_user().get_last_name()))
        return reverse_lazy('groups:group', kwargs={'group_id': self.object.group.pk})


@method_decorator(csrf_exempt, name='dispatch')
class ExchangeCodeView(TemplateView):
    template_name = 'groups/code_form.html'

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        form = forms.ExchangeCodeForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['messenger_user_id']
            code = form.cleaned_data['code']
            exchange = models.AssignationMessengerUser.objects.create(messenger_user_id=user.pk,
                                                                      group=code.group,
                                                                      code=code)
            code.exchange()
            return JsonResponse(dict(set_attributes=dict(group_code_error='false',
                                                         group_code_error_message=''),
                                     messages=[]))
        else:
            return JsonResponse(dict(set_attributes=dict(group_code_error='true',
                                                         group_code_error_message='User ID or code wrong'),
                                     messages=[]))
