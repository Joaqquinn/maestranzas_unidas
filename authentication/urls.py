from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('sin-permiso/', views.sin_permiso, name='sin_permiso'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/inventario/', views.gestor_dashboard, name='gestor_dashboard'),
    path('dashboard/compras/', views.comprador_dashboard, name='comprador_dashboard'),
    path('dashboard/almacen/', views.almacen_dashboard, name='almacen_dashboard'),
    path('dashboard/produccion/', views.produccion_dashboard, name='produccion_dashboard'),
    path('dashboard/auditor/', views.auditor_dashboard, name='auditor_dashboard'),
    path('dashboard/gerente/', views.gerente_dashboard, name='gerente_dashboard'),
    path('dashboard/usuario/', views.usuario_dashboard, name='usuario_dashboard'),

]