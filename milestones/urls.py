from django.urls import path
from milestones.views import HomeView, NewMilestoneView, MilestoneView, EditMilestoneView, response_instance_to_milestone

app_name = 'milestones'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('new/', NewMilestoneView.as_view(), name='new'),
    path('<int:id>/', MilestoneView.as_view(), name='milestone'),
    path('<int:id>/edit/', EditMilestoneView.as_view(), name='edit'),
    path('<int:id>/response/', response_instance_to_milestone, name='response')
]