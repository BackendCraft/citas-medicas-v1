from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_citas, name='lista_citas'),
    path('agregar/', views.agregar_cita, name='agregar_cita'),
    path('editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
]