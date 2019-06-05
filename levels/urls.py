from django.urls import path
from levels import views

app_name = 'levels'

urlpatterns = [
    path('', views.ListLevelView.as_view(), name='index'),
    path('new/', views.CreateLevelView.as_view(), name="new"),
    path('<int:id>/', views.LevelView.as_view(), name='level'),
    path('<int:id>/edit/', views.UpdateLevelView.as_view(), name='edit')
]
