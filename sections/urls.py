from django.urls import path
from sections import views

app_name = 'sections'

urlpatterns = [
    path('', views.ListSectionView.as_view(), name='index'),
    path('<int:id>/', views.SectionView.as_view(), name='section'),
    path('<int:id>/edit/', views.UpdateSectionView.as_view(), name='edit'),
    path('new/', views.CreateSectionView.as_view(), name='new')
]
