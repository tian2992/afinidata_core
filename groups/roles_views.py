from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from groups import models


class CreateRoleView(PermissionRequiredMixin, CreateView):
    model = models.RoleGroupUser
    permission_required = 'groups.add_rolegroupuser'
    login_url = reverse_lazy('pages:login')
    fields = ('user', 'role')

    def get_context_data(self, **kwargs):
        c = super(CreateRoleView, self).get_context_data()
        c['action'] = 'Create'
        c['group'] = get_object_or_404(models.Group, id=self.kwargs['group_id'])
        return c

    def form_valid(self, form):
        form.instance.group = get_object_or_404(models.Group, id=self.kwargs['group_id'])
        return super(CreateRoleView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'User with username: "%s" added with role: "%s" for group: "%s.' % (
            self.object.user.username,
            self.object.role,
            self.object.group.name
        ))
        return reverse_lazy('groups:group', kwargs={'group_id': self.object.group.pk})
