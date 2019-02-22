from django.urls import path
from entities.views import HomeView, NewEntityView, EditEntityView, EntityView, DeleteEntityView

app_name = 'entities'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('new/', NewEntityView.as_view(), name='new'),
    path('<int:id>/', EntityView.as_view(), name='entity'),
    path('<int:id>/edit/', EditEntityView.as_view(), name='edit'),
    path('<int:id>/delete/', DeleteEntityView.as_view(), name='delete')
]
