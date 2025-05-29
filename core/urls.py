from django.urls import path
from . import views
from books import views 


urlpatterns = [
    path('',views.index,name='index'),
]