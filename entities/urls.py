from django.urls import path
from entities.views import HomeView, NewEntityView, EditEntityView

app_name = 'entities'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('new/', NewEntityView.as_view(), name='new'),
    path('<int:id>/edit/', EditEntityView.as_view(), name='edit')
]
