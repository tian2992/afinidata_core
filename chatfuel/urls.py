from django.urls import path
from chatfuel import views

app_name = 'chatfuel'

urlpatterns = [
    path('get_user_instances/<int:id>', views.get_user_instances, name="get_user_instances")
]