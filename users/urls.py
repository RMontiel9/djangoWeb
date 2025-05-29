from django.urls import path
from . import views

from .views import CustomLoginView


urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path('login/', CustomLoginView.as_view(), name='login'),
]



