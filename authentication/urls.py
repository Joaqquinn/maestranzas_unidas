from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/inventario/', views.dashboard_inventario, name='dashboard_inventario'),
    path('dashboard/compras/', views.dashboard_compras, name='dashboard_compras'),
    path('dashboard/almacen/', views.dashboard_almacen, name='dashboard_almacen'),
    path('dashboard/produccion/', views.dashboard_produccion, name='dashboard_produccion'),
    path('dashboard/auditor/', views.dashboard_auditor, name='dashboard_auditor'),
    path('dashboard/gerente/', views.dashboard_gerente, name='dashboard_gerente'),
    path('dashboard/usuario/', views.dashboard_usuario, name='dashboard_usuario'),
    path('sin-permiso/', views.sin_permiso, name='sin_permiso'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),

]