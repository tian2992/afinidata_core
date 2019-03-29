from django.urls import path
from chatfuel import views

app_name = 'chatfuel'

urlpatterns = [
    path('get_user_instances/<int:id>/', views.get_user_instances, name='get_user_instances'),
    path('get_milestone_by_area/<int:id>/', views.milestone_by_area, name='milestone_by_area'),
    path('response_milestone_for_instance/<int:milestone_id>/', views.response_milestone_for_instance,\
         name='response_milestone_by_area'),
    path('set_area_value_to_instance/', views.set_area_value_to_instance, name='area_to_instance'),
    path('instance/new/', views.create_instance, name='new_instance'),
    path('set_sections_to_instance/', views.set_sections_by_value, name='set_sections_by_value'),
    path('evaluator/', views.Evaluator.as_view(), name='evaluator'),
    path('up_instance/<int:id>/', views.up_instance, name='up_instance')
]