from django.urls import path
from messenger_users import views

app_name = 'messenger_users'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('by_group/<str:group>/', views.ByGroupView.as_view(), name='by_group'),
    path('<int:id>/', views.UserView.as_view(), name='user'),
    path('<int:id>/set_post_group/', views.SetRandomPostGroupForUser.as_view(), name='set_post_group'),
    path('<int:id>/set_channel_id/', views.SetUserChannelID.as_view(), name='set_channel_id'),
    path('<int:id>/data/<int:attribute_id>/edit/', views.EditAttributeView.as_view(), name='attribute_edit'),
    path('<int:id>/data/<int:attribute_id>/delete/', views.DeleteAttributeView.as_view(), name='attribute_delete'),
    path('get_id_by_username/', views.GetIDByUsernameView.as_view(), name='get_id_by_username'),
    path('captcha/', views.UserCaptchaView.as_view(), name='captcha'),
    path('verify/', views.VerifyUserCaptchaView.as_view(), name='verify'),
    path('data/', views.DataView.as_view(), name='data'),
    path('delete/', views.DeleteByUsernameView.as_view(), name="delete"),
    path('<int:id>/set_attributes/', views.set_attributes_for_user, name='set_attributes'),
    path('<int:id>/assign_months_group/', views.AssignMonthsGroupView.as_view(), name='assign_months_group'),
    path('add_data/', views.CreateMessengerUserData.as_view(), name='add_data')
]