from django.urls import path
from instances import views

app_name = 'instances'

urlpatterns = [
path('', views.HomeView.as_view(), name='index'),
    path('new/', views.NewInstanceView.as_view(), name='new'),
    path('<int:id>/', views.InstanceView.as_view(), name='instance'),
    path('<int:id>/edit/', views.EditInstanceView.as_view(), name='edit'),
    path('<int:id>/delete/', views.DeleteInstanceView.as_view(), name='delete'),
    path('<int:id>/score/', views.score, name='score'),
    path('by_bot_user/<int:id>', views.instances_by_user, name='by_bot_user')
]