from django.urls import path
from messenger_users import views

app_name = 'messenger_users'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('captcha/', views.UserCaptchaView.as_view(), name='captcha'),
    path('verify/', views.VerifyUserCaptchaView.as_view(), name='verify'),
    path('data/', views.DataView.as_view(), name='data')
]