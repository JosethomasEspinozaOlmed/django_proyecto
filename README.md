# InmueblesP Y — Sistema de Compra/Venta de Inmuebles

Sistema web desarrollado con Django 5 + MySQL para el mercado paraguayo.

---

## Requisitos previos

Antes de empezar, instalá:

| Software | Versión | Descarga |
|---|---|---|
| Python | 3.11 o 3.12 | https://www.python.org/downloads/ |
| MySQL | 8.x | https://dev.mysql.com/downloads/mysql/ |
| Visual Studio Code | Última | https://code.visualstudio.com/ |
| Extensión Python (VS Code) | — | Buscar "Python" de Microsoft en Extensions |

---

## Paso 1 — Crear la base de datos en MySQL

Abrí **MySQL Workbench** o la terminal de MySQL y ejecutá:

```sql
CREATE DATABASE inmuebles_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## Paso 2 — Clonar / descomprimir el proyecto

Descomprimí la carpeta `inmuebles_py` en tu directorio de trabajo, por ejemplo:

```
C:\proyectos\inmuebles_py\
```

---

## Paso 3 — Abrir en Visual Studio Code

1. Abrí VS Code
2. `File → Open Folder` → seleccioná la carpeta `inmuebles_py`
3. Abrí la terminal integrada: `` Ctrl + ` ``

---

## Paso 4 — Configurar el archivo .env

En la terminal de VS Code:

```bat
copy .env.example .env
```

Abrí el archivo `.env` y editá estos valores con tus datos de MySQL:

```
DB_NAME=inmuebles_db
DB_USER=root
DB_PASSWORD=tu_password_de_mysql
DB_HOST=localhost
DB_PORT=3306
```

---

## Paso 5 — Ejecutar el setup automático

En la terminal de VS Code (cmd, no PowerShell):

```bat
setup.bat
```

Este script hace automáticamente:
- Crea el entorno virtual `venv/`
- Instala todas las dependencias
- Ejecuta las migraciones en MySQL
- Carga las 25 ciudades de Paraguay
- Te pide crear un superusuario (admin)

> Si la terminal dice "no se puede ejecutar scripts", cambiá a **Command Prompt**:
> En VS Code, hacé click en la flecha al lado del `+` en la terminal → "Command Prompt"

---

## Paso 6 — Activar el entorno virtual manualmente (para sesiones futuras)

Cada vez que abras VS Code, activá el entorno:

```bat
venv\Scripts\activate
```

Deberías ver `(venv)` al principio de la línea de comandos.

---

## Paso 7 — Levantar el servidor

```bat
python manage.py runserver
```

Abrí el navegador en:

| URL | Descripción |
|---|---|
| http://127.0.0.1:8000 | Sitio web principal |
| http://127.0.0.1:8000/admin | Panel de administración |

---

## Estructura del proyecto

```
inmuebles_py/
├── config/                  ← Configuración Django
│   ├── settings/
│   │   ├── base.py          ← Settings comunes
│   │   └── development.py   ← Settings de desarrollo
│   └── urls.py              ← URLs principales
├── apps/
│   ├── accounts/            ← Usuarios y perfiles
│   ├── properties/          ← Propiedades (core)
│   └── contacts/            ← Mensajes de contacto
├── templates/               ← HTML base
├── static/                  ← CSS, JS, imágenes
├── media/                   ← Uploads de usuarios
├── requirements/
│   ├── base.txt             ← Dependencias base
│   └── development.txt      ← Dependencias de desarrollo
├── .env                     ← Variables de entorno (NO subir a git)
├── manage.py
└── setup.bat                ← Script de instalación
```

---

## Comandos útiles del día a día

```bat
# Activar entorno virtual
venv\Scripts\activate

# Levantar servidor de desarrollo
python manage.py runserver

# Crear migraciones después de cambiar modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario nuevo
python manage.py createsuperuser

# Abrir shell de Django para probar código
python manage.py shell

# Cargar ciudades (si se borran)
python manage.py loaddata apps/properties/fixtures/cities.json
```

---

## Flujo de uso del sistema

### Como comprador
1. Registrarse en `/accounts/signup/`
2. Buscar propiedades en la página principal
3. Ver el detalle y enviar mensaje al vendedor

### Como vendedor
1. Registrarse y luego ir a **Mi perfil**
2. Cambiar el rol a **Vendedor**
3. Ir a **Publicar propiedad** y completar el formulario
4. Gestionar las publicaciones desde **Mis publicaciones**

---

## Configuración de VS Code recomendada

Creá el archivo `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

---

## Solución de problemas comunes

### Error: `mysqlclient` no instala en Windows
```bat
pip install mysqlclient --only-binary :all:
```
Si sigue fallando, descargá el `.whl` desde:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Error: `No module named 'apps'`
Asegurate de ejecutar los comandos desde la carpeta raíz del proyecto
(donde está `manage.py`).

### Error al conectar MySQL
Verificá que el servicio MySQL esté corriendo:
- `Win + R` → `services.msc` → buscá "MySQL80" → iniciar

### Puerto 8000 ocupado
```bat
python manage.py runserver 8001
```

---

## Dependencias instaladas

| Paquete | Versión | Función |
|---|---|---|
| Django | 5.0.6 | Framework principal |
| mysqlclient | 2.2.4 | Conector MySQL |
| Pillow | 10.3.0 | Procesamiento de imágenes |
| django-crispy-forms | 2.1 | Formularios con Bootstrap |
| crispy-bootstrap5 | 2024.2 | Template pack Bootstrap 5 |
| django-allauth | 0.63.3 | Autenticación completa |
| django-filter | 24.2 | Filtros de búsqueda |
| djangorestframework | 3.15.1 | API REST |
| python-decouple | 3.8 | Variables de entorno |
| whitenoise | 6.7.0 | Archivos estáticos |
