from django.urls import path
from groups import views

app_name = 'groups'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='groups'),
    path('<int:group_id>/', views.GroupView.as_view(), name='group'),
    path('add/', views.CreateGroupView.as_view(), name='add')
]
