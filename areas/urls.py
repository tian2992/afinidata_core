from django.urls import path
from areas import views

app_name = 'areas'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('new/', views.NewAreaView.as_view(), name='new'),
    path('<int:id>/', views.AreaView.as_view(), name='area'),
    path('<int:id>/edit/', views.EditAreaView.as_view(), name='edit'),
    path('<int:id>/delete/', views.DeleteAreaView.as_view(), name='delete'),
    path('<int:id>/milestones/', views.milestones_by_area, name='milestones')
]
