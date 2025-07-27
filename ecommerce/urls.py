from django.urls import path
from .views import home, crear_cliente, crear_producto, registro, login_view, logout_view, busqueda

urlpatterns = [
    path('', home, name='home'),
    path('crear_cliente/', crear_cliente, name='crear_cliente'),
    path('crear-producto/', crear_producto, name='crear_producto'),
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('busqueda/', busqueda, name='busqueda'),
]