from django.urls import path
from bots import views

app_name = 'bots'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('new/', views.CreateBotView.as_view(), name='new'),
    path('<int:id>', views.BotView.as_view(), name='bot'),
    path('<int:id>/edit/', views.UpdateBotView.as_view(), name='edit'),
    path('<int:id>/delete/', views.DeleteBotView.as_view(), name='delete')
]