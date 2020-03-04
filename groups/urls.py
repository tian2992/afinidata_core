from django.urls import path
from groups import views
from groups import roles_views
from groups import messenger_users_views

app_name = 'groups'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='groups'),
    path('<int:group_id>/', views.GroupView.as_view(), name='group'),
    path('<int:group_id>/add_user/', roles_views.CreateRoleView.as_view(), name='add_user_group'),
    path('<int:group_id>/add_messenger_user/', messenger_users_views.AddMessengerUserView.as_view(),
         name='add__messenger_user_group'),
    path('add/', views.CreateGroupView.as_view(), name='add')
]
