from django.urls import path
from instances import views
from instances import service_views

app_name = 'instances'

urlpatterns = [
path('', views.HomeView.as_view(), name='index'),
    path('new/', views.NewInstanceView.as_view(), name='new'),
    path('<int:id>/', views.InstanceView.as_view(), name='instance'),
    path('<int:id>/edit/', views.EditInstanceView.as_view(), name='edit'),
    path('<int:id>/delete/', views.DeleteInstanceView.as_view(), name='delete'),
    path('<int:id>/add_attribute/', views.AddAttributeToInstance.as_view(), name="add_attribute"),
    path('<int:id>/add_section/', views.InstanceSectionView.as_view(), name="add_section"),
    path('<int:id>/evaluator/', views.Evaluator.as_view(), name="evaluator"),
    path('<int:id>/up/', views.up_instance, name='up'),
    path('<int:id>/get_activity/', views.GetActivityView.as_view(), name='get_activity'),
    path('score/', views.score, name='score'),
    path('by_bot_user/<int:id>/', views.instances_by_user, name='by_bot_user'),
    path('<int:id>/milestone/', service_views.milestone_by_area, name='milestone_by_area'),
    path('api/new/', service_views.create_user, name="api_user"),
    path('<int:instance_id>/create_attribute/', service_views.CreateInstanceAttributeView.as_view(),
         name='create_attribute')
]