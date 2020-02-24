from django.urls import path
from utilities import views

app_name = 'utilities'

urlpatterns = [
    path('get_children/', views.GetChildrenView.as_view(), name='get_children'),
    path('get_children_milestones/', views.GetChildrenMilestonesView.as_view(), name='get_children_milestones')
]
