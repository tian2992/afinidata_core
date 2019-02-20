from django.urls import path
from areas.views import NewAreaView, HomeView, AreaView, EditAreaView

app_name = 'areas'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('new/', NewAreaView.as_view(), name='new'),
    path('<int:id>/', AreaView.as_view(), name='area'),
    path('<int:id>/edit/', EditAreaView.as_view(), name='edit')
]
