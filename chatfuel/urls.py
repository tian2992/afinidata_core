from django.urls import path
from chatfuel import views

app_name = 'chatfuel'

urlpatterns = [
    path('create_messenger_user/', views.CreateMessengerUserView.as_view(), name='create_messenger_user'),
    path('create_messenger_user_data/', views.CreateMessengerUserDataView.as_view(), name='create_messenger_user_data'),
    path('instance/new/', views.create_instance, name='new_instance'),
    path('get_instances/', views.GetInstancesByUserView.as_view(), name='get_instances'),
    path('verify_code/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('exchange_code/', views.ExchangeCodeView.as_view(), name='exchange_code')
]