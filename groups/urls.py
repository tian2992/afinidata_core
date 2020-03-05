from django.urls import path
from groups import views
from groups import roles_views
from groups import messenger_users_views
from groups import codes_views

app_name = 'groups'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='groups'),
    path('<int:group_id>/', views.GroupView.as_view(), name='group'),
    path('<int:group_id>/add_user/', roles_views.CreateRoleView.as_view(), name='add_user_group'),
    path('<int:group_id>/add_messenger_user/', messenger_users_views.AddMessengerUserView.as_view(),
         name='add__messenger_user_group'),
    path('<int:group_id>/add_code/', codes_views.CreateCodeView.as_view(), name='add_code_group'),
    path('add/', views.CreateGroupView.as_view(), name='add'),
    path('exchange_code/', messenger_users_views.ExchangeCodeView.as_view(), name='exchange_code')
]
