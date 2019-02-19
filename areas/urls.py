from django.urls import path
from areas.views import NewAreaView, HomeView

app_name = 'areas'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('new/', NewAreaView.as_view(), name='new')
]
