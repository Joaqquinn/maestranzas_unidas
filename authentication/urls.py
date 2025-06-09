from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sin-permiso/', views.sin_permiso, name='sin_permiso'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]