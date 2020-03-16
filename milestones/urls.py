from django.urls import path
from milestones import views

app_name = 'milestones'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('new/', views.NewMilestoneView.as_view(), name='new'),
    path('<int:id>/', views.MilestoneView.as_view(), name='milestone'),
    path('<int:id>/edit/', views.EditMilestoneView.as_view(), name='edit')
]
