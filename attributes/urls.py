from django.urls import path
from attributes import views

app_name = 'attributes'

urlpatterns = [
    path('', views.AttributesView.as_view(), name="index"),
    path('new/', views.NewAttributeView.as_view(), name="new"),
    path('<int:id>/', views.AttributeView.as_view(), name="attribute"),
    path('<int:id>/edit/', views.EditAttributeView.as_view(), name='edit')
]
