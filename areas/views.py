from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, UpdateView
from areas.forms import AreaFormModel
from areas.models import Area


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
            form.save()
            return redirect('areas:index')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = AreaFormModel(request.POST or None)

        return render(request, self.template_name, {'form': form})
