# 🛒 Sistema Gestor de E-commerce en Django

Un sistema integral de gestión de clientes y productos desarrollado con Django 5.2, que incluye autenticación personalizada, búsqueda avanzada y sistema VIP para clientes.

## 📋 Características

- **🔐 Autenticación personalizada** con hash SHA256
- **👥 Gestión completa de clientes** con sistema VIP automático
- **📦 Catálogo de productos** con control de stock y estado
- **🔍 Búsqueda avanzada** con filtros por tipo
- **💎 Sistema VIP** para clientes mayores de 40 años
- **🎨 Interfaz moderna** con CSS organizado y Font Awesome
- **📱 Diseño responsive** para todos los dispositivos

## 🛠️ Tecnologías

- **Backend:** Django 5.2.4
- **Base de datos:** SQLite3
- **Frontend:** HTML5, CSS3, Font Awesome 6.4.0
- **Seguridad:** Hash SHA256 para contraseñas
- **Arquitectura:** MVT (Modelo-Vista-Template)

## 📁 Estructura del Proyecto

```
TuPrimeraPagina_Agresta/
├── db.sqlite3                 # Base de datos SQLite
├── manage.py                  # Comando principal de Django
├── requirements.txt           # Dependencias del proyecto
├── ecommerce/                 # Aplicación principal
│   ├── models.py             # Modelos de datos
│   ├── views.py              # Lógica de negocio
│   ├── urls.py               # Rutas de la aplicación
│   ├── forms.py              # Formularios
│   ├── admin.py              # Configuración del admin
│   ├── templates/commerce/   # Templates HTML
│   ├── fixtures/             # Datos de prueba
│   │   ├── products.json     # 15 productos de ejemplo
│   │   └── clients.json      # 10 clientes de prueba
│   └── management/commands/  # Comandos personalizados
├── tercera_entrega/          # Configuración del proyecto
│   ├── settings.py           # Configuraciones
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Configuración WSGI
└── static/css/               # Archivos CSS organizados
    ├── base.css              # Estilos base
    ├── auth.css              # Estilos de autenticación
    ├── forms.css             # Estilos de formularios
    └── search.css            # Estilos de búsqueda
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd TuPrimeraPagina_Agresta
```

### 2. Crear y activar entorno virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. **⚡ Cargar datos de prueba (RECOMENDADO)**
Para comenzar a usar el sistema inmediatamente con datos de ejemplo:

```bash
# Cargar productos de prueba (15 productos variados)
python manage.py loaddata ecommerce/fixtures/products.json

# Cargar clientes de prueba (10 clientes incluyendo VIP)
python manage.py loaddata ecommerce/fixtures/clients.json
```

**📋 Datos incluidos:**
- **Productos:** 15 productos variados con precios, stock y descripciones reales
- **Clientes:** 10 clientes de diferentes edades (algunos VIP mayores de 40 años)
- **Categorías:** Electrónicos, cámaras de seguridad, tecnología, etc.

💡 **Tip:** Estos datos te permitirán probar inmediatamente la búsqueda, filtros y sistema VIP sin tener que crear contenido manualmente.

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000` para ver la aplicación.

## 👤 Uso del Sistema

> **💡 Datos de Prueba:** Si cargaste los fixtures en el paso 5, ya tendrás 15 productos y 10 clientes disponibles para probar todas las funcionalidades del sistema, incluyendo la búsqueda y el sistema VIP.

### Registro e Inicio de Sesión
1. **Registro:** Crea una cuenta en `/registro/` con usuario, email y contraseña
2. **Login:** Inicia sesión en `/login/` con email y contraseña
3. **Logout:** Cierra sesión desde el menú de navegación

### Gestión de Clientes
- **Crear cliente:** Formulario con validación de email único
- **Sistema VIP:** Detección automática para mayores de 40 años
- **Búsqueda:** Encuentra clientes por nombre o email

### Gestión de Productos
- **Crear producto:** Formulario completo con precio, stock y descripción
- **Estado activo/inactivo:** Control de visibilidad de productos
- **Búsqueda:** Encuentra productos por nombre o descripción

### Búsqueda Avanzada
- **Búsqueda general:** Busca en clientes y productos simultáneamente
- **Filtros específicos:** Solo clientes, solo productos, o ambos
- **Búsqueda insensible:** No distingue mayúsculas y minúsculas

## 📊 Modelos de Datos

### UsuarioSistema
- `usuario`: Nombre de usuario único
- `email`: Correo electrónico único
- `password`: Contraseña hasheada (SHA256)
- `created_at`: Fecha de registro
- `is_active`: Estado del usuario

### Cliente
- `name`: Nombre completo
- `age`: Edad (determina status VIP)
- `email`: Correo electrónico único
- `created_at`: Fecha de registro

### Producto
- `nombre`: Nombre del producto
- `precio`: Precio con validación mínima
- `descripcion`: Descripción detallada
- `stock`: Cantidad disponible
- `activo`: Estado de visibilidad
- `created_at`: Fecha de creación

## 🔧 Comandos Útiles

### Gestión de datos de prueba
```bash
# Cargar datos de prueba inicial
python manage.py loaddata ecommerce/fixtures/products.json
python manage.py loaddata ecommerce/fixtures/clients.json

# Exportar datos actuales para backup
python manage.py dumpdata ecommerce.Producto --indent 2 > backup_products.json
python manage.py dumpdata ecommerce.Cliente --indent 2 > backup_clients.json

# Resetear y recargar datos (⚠️ Elimina datos existentes)
python manage.py flush --noinput
python manage.py loaddata ecommerce/fixtures/products.json ecommerce/fixtures/clients.json
```

### Limpieza de sesiones
```bash
# Limpiar sesiones expiradas
python manage.py clearsessions

# Limpiar todas las sesiones (comando personalizado)
python manage.py clear_all_sessions --all
```

### Gestión de archivos estáticos
```bash
# Recopilar archivos estáticos para producción
python manage.py collectstatic
```

### Base de datos
```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones específicas
python manage.py migrate ecommerce
```

## 🎨 Personalización CSS

El proyecto utiliza una arquitectura CSS modular:

- **`base.css`**: Estilos globales y layout principal
- **`auth.css`**: Formularios de login y registro
- **`forms.css`**: Formularios de creación de clientes y productos
- **`search.css`**: Interfaz de búsqueda y resultados

Para modificar estilos, edita los archivos en `/static/css/` y ejecuta:
```bash
python manage.py collectstatic
```

## 🔒 Seguridad

- **Contraseñas hasheadas** con SHA256
- **Validación CSRF** habilitada
- **Validación de formularios** en backend
- **Sesiones seguras** con expiración configurable
- **Emails únicos** para usuarios y clientes

## 🐛 Solución de Problemas

### Problema: Sesiones persisten entre reinicios
**Solución:** Ejecutar `python manage.py clear_all_sessions --all`

### Problema: CSS no se aplica
**Solución:** Verificar `STATICFILES_DIRS` en `settings.py` y ejecutar `collectstatic`

### Problema: Error de migraciones
**Solución:** 
```bash
python manage.py makemigrations --empty ecommerce
python manage.py migrate
```

## 🚀 Despliegue en Producción

### Cambios requeridos en `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
SECRET_KEY = 'nueva-clave-secreta-segura'
```

### Configurar base de datos PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_base_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📄 Licencia

Este proyecto está desarrollado con fines educativos.

## 👥 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

- **Desarrollador:** Daniel Agresta
- **Email:** leinadatserga@gmail.com
- **GitHub:** https://github.com/leinadatserga

---

⭐ **¡Dale una estrella al proyecto si te resultó útil!**
