from django.urls import path
from entities import views

app_name = 'entities'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('new/', views.NewEntityView.as_view(), name='new'),
    path('<int:id>/', views.EntityView.as_view(), name='entity'),
    path('<int:id>/edit/', views.EditEntityView.as_view(), name='edit'),
    path('<int:id>/delete/', views.DeleteEntityView.as_view(), name='delete'),
    path('<int:id>/add_attribute/', views.AddAttributeToEntityView.as_view(), name='add_attribute')
]
