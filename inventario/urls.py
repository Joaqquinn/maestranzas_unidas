from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pieza/nueva/', views.PiezaCreateView.as_view(), name='pieza_create'),
    path('listar/', views.listar_piezas, name='listar_piezas'),
    path('pieza/<int:pk>/', views.pieza_detalle, name='pieza_detalle'),
    path('registrar_movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
]

