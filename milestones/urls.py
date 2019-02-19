from django.urls import path
from milestones.views import HomeView, NewMilestoneView

app_name = 'milestones'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('new/', NewMilestoneView.as_view(), name='new')
]