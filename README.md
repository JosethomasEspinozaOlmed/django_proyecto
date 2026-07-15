# InmueblesPY

Sistema web inmobiliario desarrollado con Django, orientado a la publicación, búsqueda y gestión de propiedades. El sistema permite que una persona pueda crear una cuenta y utilizarla tanto como comprador como vendedor, facilitando la publicación de inmuebles y el contacto entre usuarios interesados.

## Descripción del proyecto

InmueblesPY es una plataforma web que permite a los usuarios registrarse, iniciar sesión, publicar propiedades, administrar sus publicaciones y contactar a vendedores. El sistema cuenta con un diseño responsivo, validaciones en formularios, búsqueda de propiedades, filtros, ubicación mediante mapa interactivo y gestión de mensajes entre compradores y vendedores.

El proyecto fue desarrollado como parte de un trabajo grupal utilizando Django como framework principal.

## Funcionalidades principales

* Registro de usuarios.
* Inicio y cierre de sesión.
* Cuenta con doble rol: comprador y vendedor.
* Publicación de propiedades.
* Edición de publicaciones.
* Eliminación de publicaciones.
* Activación y pausa de publicaciones.
* Listado de propiedades disponibles.
* Página de detalle de cada propiedad.
* Buscador y filtros por tipo, departamento, moneda y precio.
* Formulario de publicación con validaciones.
* Precio con separador de miles.
* Selección de departamento y ciudad relacionada.
* Ubicación mediante mapa interactivo.
* Carga de imagen principal.
* Contacto con el vendedor.
* Visualización de mensajes recibidos.
* Diseño responsivo para computadoras y celulares.

## Tecnologías utilizadas

* Python
* Django
* SQLite
* HTML
* CSS
* Bootstrap
* JavaScript
* Leaflet
* OpenStreetMap
* Pillow

## Estructura principal del proyecto

```text
django_proyecto/
│
├── apps/
│   ├── usuarios/
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── propiedades/
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── data.py
│   │   └── migrations/
│   │
│   └── contactos/
│       ├── models.py
│       ├── forms.py
│       ├── views.py
│       └── urls.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── templates/
│   ├── base.html
│   ├── registration/
│   │   └── registro.html
│   ├── propiedades/
│   │   ├── formulario.html
│   │   ├── mis_publicaciones.html
│   │   └── detalle.html
│   └── contactos/
│
├── static/
│   └── css/
│       └── styles.css
│
├── media/
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## Módulos del sistema

### Módulo de usuarios

Permite el registro, inicio de sesión y cierre de sesión. Cada usuario posee un perfil asociado con los campos `es_comprador` y `es_vendedor`, permitiendo que una misma cuenta pueda comprar y publicar propiedades.

Archivos principales:

```text
apps/usuarios/models.py
apps/usuarios/forms.py
apps/usuarios/views.py
apps/usuarios/urls.py
templates/registration/registro.html
```

### Módulo de propiedades

Permite publicar, editar, eliminar, activar, pausar, listar y visualizar propiedades. También incluye validaciones del formulario, manejo de imágenes, precio con formato, ubicación mediante mapa y carga dinámica de ciudades por departamento.

Archivos principales:

```text
apps/propiedades/models.py
apps/propiedades/forms.py
apps/propiedades/views.py
apps/propiedades/urls.py
apps/propiedades/data.py
templates/propiedades/formulario.html
templates/propiedades/mis_publicaciones.html
templates/propiedades/detalle.html
```

### Módulo de contactos

Permite que un comprador envíe un mensaje al vendedor de una propiedad. También permite que el vendedor pueda visualizar los mensajes recibidos en sus publicaciones.

Archivos principales:

```text
apps/contactos/models.py
apps/contactos/forms.py
apps/contactos/views.py
apps/contactos/urls.py
templates/contactos/contactar.html
templates/contactos/mensajes_recibidos.html
```

## Modelo de datos principal

El sistema trabaja principalmente con las siguientes entidades:

* Usuario
* Perfil
* Propiedad
* Contacto

Relaciones principales:

* Un usuario tiene un perfil.
* Un usuario puede publicar muchas propiedades.
* Una propiedad pertenece a un vendedor.
* Un usuario puede enviar muchos mensajes de contacto.
* Una propiedad puede recibir muchos mensajes de contacto.

## Requisitos para ejecutar el proyecto

Antes de ejecutar el proyecto, se recomienda tener instalado:

* Python 3.12
* pip
* virtualenv
* Git

## Instalación y ejecución

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar a la carpeta del proyecto:

```bash
cd django_proyecto
```

Crear el entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual en Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecutar:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego activar nuevamente:

```bash
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar las migraciones:

```bash
python manage.py migrate
```

Crear un superusuario:

```bash
python manage.py createsuperuser
```

Ejecutar el servidor:

```bash
python manage.py runserver
```

Abrir el sistema en el navegador:

```text
http://127.0.0.1:8000/
```

## Comandos útiles

Verificar errores del proyecto:

```bash
python manage.py check
```

Crear migraciones:

```bash
python manage.py makemigrations
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Ejecutar el servidor:

```bash
python manage.py runserver
```

Limpiar registros de la base de datos:

```bash
python manage.py flush
```

Crear un administrador:

```bash
python manage.py createsuperuser
```

## Dependencias principales

El archivo `requirements.txt` debe incluir las dependencias necesarias para ejecutar el proyecto. Las principales son:

```text
Django==4.2.25
Pillow
```

## Roles de usuario

El sistema permite que un usuario tenga ambos roles al mismo tiempo:

* Comprador
* Vendedor

Esto significa que una misma cuenta puede publicar propiedades y también contactar a otros vendedores.

## Integrantes y división del trabajo

### José

Responsable principal del módulo de propiedades, diseño general y funcionalidades relacionadas con la publicación de inmuebles.

Tareas principales:

* Diseño general del sistema.
* Plantilla base del sitio.
* Formulario de publicación.
* Validaciones de propiedades.
* Precio con separador de miles.
* Mapa interactivo.
* CRUD de propiedades.
* Página principal con filtros y búsqueda.

### Gastón

Responsable principal del módulo de usuarios y administración de publicaciones.

Tareas principales:

* Registro de usuarios.
* Inicio y cierre de sesión.
* Perfil con rol comprador y vendedor.
* Validación de correo, teléfono y contraseña.
* Página de Mis publicaciones.
* Filtros de publicaciones activas y pausadas.
* Datos de departamentos y ciudades.
* Rutas del módulo de propiedades.

### Jorge

Responsable principal de la base de datos, detalle de propiedades y módulo de contactos.

Tareas principales:

* Modelo de propiedades.
* Migraciones.
* Detalle de propiedad.
* Mapa en la vista de detalle.
* Modelo de contactos.
* Formulario de contacto.
* Mensajes recibidos.
* Configuración de archivos multimedia.

## Flujo general del sistema

1. El usuario se registra.
2. El sistema crea automáticamente su perfil como comprador y vendedor.
3. El usuario puede publicar una propiedad.
4. El sistema valida los datos ingresados.
5. La propiedad queda visible en la página principal si está activa.
6. Otros usuarios pueden ver el detalle de la propiedad.
7. Un comprador puede contactar al vendedor.
8. El vendedor puede revisar los mensajes recibidos.
9. El vendedor puede editar, pausar, activar o eliminar sus publicaciones.

## Estado del proyecto

El sistema se encuentra en etapa funcional, con las principales funcionalidades implementadas:

* Registro de usuarios.
* Publicación de propiedades.
* Administración de publicaciones.
* Búsqueda y filtros.
* Contacto entre comprador y vendedor.
* Diseño responsivo.
* Ubicación mediante mapa interactivo.

