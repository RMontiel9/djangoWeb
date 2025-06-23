from django.urls import path
from . import views

urlpatterns = [
    path('favoritos/toggle/', views.toggle_favorito, name='agregar_favorito'),
    path('<str:google_id>/', views.book_detail, name='book_detail'),
    ]
