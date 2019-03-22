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
    path('score/', views.score, name='score'),
    path('by_bot_user/<int:id>/', views.instances_by_user, name='by_bot_user'),
    path('api/new/', service_views.create_user, name="api_user")
]