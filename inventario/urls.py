from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pieza/nueva/', views.PiezaCreateView.as_view(), name='pieza_create'),
    path('listar/', views.lista_piezas, name='listar_piezas'),
    path('pieza/<int:pk>/', views.pieza_detalle, name='pieza_detalle'),
    path('registrar_movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('lotes/registrar/', views.registrar_lote, name='registrar_lote'),
    path('precios/registrar/', views.registrar_precio, name='registrar_precio'),
    path('pieza/<int:pk>/editar/', views.editar_pieza, name='editar_pieza'),
]

