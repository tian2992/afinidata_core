from django.urls import path
from forms import views

app_name = 'forms'

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('new/', views.CreateFormView.as_view(), name="new"),
    path('<int:id>/', views.FormView.as_view(), name="form"),
    path('<int:id>/edit/', views.UpdateFormView.as_view(), name="edit"),
    path('<int:id>/add_attribute/', views.AddAttributeToForm.as_view(), name="add_attribute"),
    path('validations/<int:id>/', views.ValidationView.as_view(), name="validation"),
    path('validations/<int:id>/edit/', views.ValidationEditView.as_view(), name="validation-edit")
]
