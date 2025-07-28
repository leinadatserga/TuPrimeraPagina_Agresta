from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.utils import timezone
from functools import wraps
from .forms import formularioCliente, formularioProductos, formularioRegistro, formularioLogin
from .models import Cliente, Producto, UsuarioSistema
import hashlib


def debug_session_info(request):
    """
    Función de utilidad para depuración de sesiones.
    Muestra información detallada sobre la sesión actual.
    Solo para desarrollo - no usar en producción.
    """
    if hasattr(request, 'session'):
        session_key = request.session.session_key
        user_id = request.session.get('user_id')
        username = request.session.get('username')
        
        active_sessions = Session.objects.filter(expire_date__gt=timezone.now()).count()
        
        print(f"=== DEBUG SESIÓN ===")
        print(f"Session Key: {session_key}")
        print(f"User ID: {user_id}")
        print(f"Username: {username}")
        print(f"Sesiones activas totales: {active_sessions}")
        print(f"==================")


def login_required_custom(view_func):
    """
    Componente (decorador) especializado para requerir login.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    """
    Vista principal del sistema e-commerce.
    Renderiza la página de inicio con información general del sistema.
    No requiere autenticación.
    """
    return render(request, 'commerce/home.html')

@login_required_custom
def crear_cliente(request):
    """
    Vista para crear nuevos clientes en el sistema.
    Muestra el formulario de creación de clientes con validación.
    Requiere autenticación.
    Features:
        - Validación de email único.
        - Detección automática de clientes VIP.
        - Mensajes informativos de estado.
        - Manejo de errores de duplicación.
    """
    if request.method == 'POST':
        form = formularioCliente(request.POST)
        if form.is_valid():
            # Extraer datos del formulario.
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            
            try:
                # Crear el cliente en la base de datos.
                cliente = Cliente.objects.create(
                    name=name,
                    age=age,
                    email=email
                )
                
                messages.success(request, f'Cliente "{name}" creado exitosamente!')
                
                # Información sobre quién lo creó.
                username = request.session.get('username', 'Usuario')
                messages.info(request, f'Cliente registrado por: {username}')
                
                # Verificar si es VIP y mostrar mensaje adicional.
                if age > 40:
                    messages.info(request, f'¡{name} es un cliente VIP por ser mayor de 40 años!')
                
                # Redirigir para limpiar el formulario.
                return redirect('crear_cliente')
                
            except Exception as e:
                # Manejar errores.
                messages.error(request, 'Error al crear el cliente. Verifique que el email no esté duplicado.')
    else:
        form = formularioCliente()
    
    return render(request, 'commerce/crear_cliente.html', {'form': form})

@login_required_custom
def crear_producto(request):
    """
    Vista para crear nuevos productos en el catálogo.
    Presenta el formulario de creación de productos con validación completa.
    Requiere autenticación.
    Features:
        - Validación de campos obligatorios y formato.
        - Control de stock y precios.
        - Estado activo/inactivo para visibilidad.
        - Mensajes informativos según el estado.
    """
    if request.method == 'POST':
        form = formularioProductos(request.POST)
        if form.is_valid():
            # Extraer los datos del formulario.
            nombre = form.cleaned_data['nombre']
            precio = form.cleaned_data['precio']
            descripcion = form.cleaned_data['descripcion']
            stock = form.cleaned_data['stock']
            activo = form.cleaned_data['activo']
            
            try:
                # Crear el producto en la base de datos.
                producto = Producto.objects.create(
                    nombre=nombre,
                    precio=precio,
                    descripcion=descripcion,
                    stock=stock,
                    activo=activo
                )
                
                messages.success(request, f'Producto "{nombre}" creado exitosamente!')
                
                # Información sobre quién lo creó.
                username = request.session.get('username', 'Usuario')
                messages.info(request, f'Producto registrado por: {username}')
                
                # Mensaje adicional según el estado.
                if activo:
                    messages.info(request, f'El producto está activo y disponible.')
                else:
                    messages.warning(request, f'El producto está inactivo y no será visible.')
                
                # Redirección para limpiar el formulario.
                return redirect('crear_producto')
                
            except Exception as e:
                # Manejo de errores.
                messages.error(request, 'Error al crear el producto. Verifique los datos ingresados.')
    else:
        form = formularioProductos()
    
    return render(request, 'commerce/crear_producto.html', {'form': form})


def registro(request):
    """
    Vista para registro de nuevos usuarios en el sistema.
    Permite a nuevos usuarios crear una cuenta con validación completa.
    Incluye hash seguro de contraseñas y login automático tras registro.
    Features:
        - Validación de email y usuario único.
        - Creación de sesión automática.
        - Contraseñas hasheadas antes del almacenamiento.
        - Validación de campos únicos (email, usuario).
    """
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        if form.is_valid():
            try:
                # Aplicación del hash a la contraseña.
                password_hash = hashlib.sha256(form.cleaned_data['password1'].encode()).hexdigest()
                
                user = UsuarioSistema.objects.create(
                    usuario=form.cleaned_data['usuario'],
                    email=form.cleaned_data['email'],
                    password=password_hash
                )
                
                username = form.cleaned_data['usuario']
                messages.success(request, f'¡Usuario "{username}" creado exitosamente!')
                
                # Guardar datos en sesión para simular login.
                request.session['user_id'] = user.id
                request.session['username'] = user.usuario
                request.session['email'] = user.email
                
                messages.info(request, f'¡Bienvenido {username}! Has iniciado sesión automáticamente.')
                
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Error al crear el usuario. Verifique que el email y nombre de usuario no estén duplicados.')
    else:
        form = formularioRegistro()
    
    return render(request, 'commerce/registro.html', {'form': form})


def login_view(request):
    """
    Vista para autenticación de usuarios existentes.
    Maneja el proceso de login con validación de credenciales.
    Features:
        - Autenticación por email y contraseña.
        - Verificación de usuario activo.
        - Creación de sesión segura.
        - Verificación de contraseña hasheada.
        - Control de usuarios activos únicamente.
    """
    if request.method == 'POST':
        form = formularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                user = UsuarioSistema.objects.get(email=email, password=password_hash, is_active=True)
                
                # Guardar datos en sesión.
                request.session['user_id'] = user.id
                request.session['username'] = user.usuario
                request.session['email'] = user.email
                
                messages.success(request, f'¡Bienvenido {user.usuario}!')
                return redirect('home')
                
            except UsuarioSistema.DoesNotExist:
                messages.error(request, 'Credenciales incorrectas. Verifique su email y contraseña.')
    else:
        form = formularioLogin()
    
    return render(request, 'commerce/login.html', {'form': form})


def logout_view(request):
    """
    Vista para cerrar sesión de usuarios.
    Limpia completamente la sesión del usuario y muestra mensaje de despedida.
    Features:
        - Mensaje personalizado de despedida.
        - Redirección segura a la página principal.
        - Eliminación completa de datos de sesión.
        - No exposición de información sensible.
    """
    username = request.session.get('username', 'Usuario')
    
    # Limpiar la sesión.
    request.session.flush()
    
    messages.info(request, f'¡Hasta luego {username}! Has cerrado sesión correctamente.')
    return redirect('home')


@login_required_custom
def busqueda(request):
    """
    Vista para búsqueda avanzada de clientes y productos.
    Permite búsqueda flexible por texto libre con filtros por tipo.
    Utiliza Django Q objects para búsquedas complejas e insensibles a mayúsculas.
    Features:
        - Clientes: búsqueda por nombre y email.
        - Productos: búsqueda por nombre y descripción.
        - Búsqueda insensible a mayúsculas/minúsculas.
        - Estadísticas de resultados en tiempo real.
    """
    query = request.GET.get('q', '').strip()
    tipo_busqueda = request.GET.get('tipo', 'todos')
    
    clientes = []
    productos = []
    
    if query:
        if tipo_busqueda == 'clientes' or tipo_busqueda == 'todos':
            # Buscar en clientes por nombre o email.
            clientes = Cliente.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query)
            ).order_by('name')
        
        if tipo_busqueda == 'productos' or tipo_busqueda == 'todos':
            # Buscar en productos por nombre o descripción.
            productos = Producto.objects.filter(
                Q(nombre__icontains=query) | 
                Q(descripcion__icontains=query)
            ).order_by('nombre')
        
        # Mensajes informativos.
        total_resultados = len(clientes) + len(productos)
        if total_resultados > 0:
            messages.success(request, f'Se encontraron {total_resultados} resultado(s) para "{query}"')
        else:
            messages.warning(request, f'No se encontraron resultados para "{query}"')
    
    context = {
        'query': query,
        'tipo_busqueda': tipo_busqueda,
        'clientes': clientes,
        'productos': productos,
        'total_clientes': len(clientes),
        'total_productos': len(productos),
    }
    
    return render(request, 'commerce/busqueda.html', context)