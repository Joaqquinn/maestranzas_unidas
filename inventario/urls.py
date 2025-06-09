from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pieza/nueva/', views.PiezaCreateView.as_view(), name='pieza_create'),
    path('listar/', views.lista_piezas, name='listar_piezas'),
    path('pieza/<int:pk>/', views.pieza_detalle, name='pieza_detalle'),
    path('registrar_movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('precios/registrar/', views.registrar_precio, name='registrar_precio'),
    path('pieza/<int:pk>/editar/', views.editar_pieza, name='editar_pieza'),
    path('ubicaciones/', views.listar_ubicaciones, name='listar_ubicaciones'),
    path('ubicaciones/nueva/', views.crear_ubicacion, name='crear_ubicacion'),
    path('ubicaciones/<int:pk>/editar/', views.editar_ubicacion, name='editar_ubicacion'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Importado desde views de inventario
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('proveedores/nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('lotes/', views.listar_lotes, name='listar_lotes'),
    path('lotes/nuevo/', views.registrar_lote, name='agregar_lote'),
    path('kits/', views.listar_kits, name='listar_kits'),
    path('kits/nuevo/', views.crear_kit, name='crear_kit'),
    path('kits/editar/<int:pk>/', views.editar_kit, name='editar_kit'),
    path('kits/eliminar/<int:pk>/', views.eliminar_kit, name='eliminar_kit'),
    path('kits/salida/', views.registrar_salida_kit, name='registrar_salida_kit'),
    path('reportes/', views.reportes_personalizados, name='reportes_personalizados'),
    path('reportes/exportar-excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
    path('reportes/exportar-pdf/', views.exportar_reporte_pdf, name='exportar_reporte_pdf'),
]



