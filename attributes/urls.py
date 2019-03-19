from django.urls import path
from attributes import views

app_name = 'attributes'

urlpatterns = [
    path('', views.AttributesView.as_view(), name="attributes-list"),
    path('new/', views.NewAttributeView.as_view(), name="attributes-new")
]
