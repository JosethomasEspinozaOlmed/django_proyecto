@echo off
echo ============================================================
echo   InmueblesP Y — Setup inicial (Windows)
echo ============================================================
echo.

REM 1. Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Descargalo desde https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python encontrado.

REM 2. Crear entorno virtual
if not exist "venv" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado.
) else (
    echo [OK] Entorno virtual ya existe.
)

REM 3. Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM 4. Instalar dependencias
echo [INFO] Instalando dependencias...
pip install --upgrade pip -q
pip install -r requirements/development.txt
echo [OK] Dependencias instaladas.

REM 5. Crear archivo .env si no existe
if not exist ".env" (
    echo [INFO] Creando archivo .env desde .env.example...
    copy .env.example .env
    echo.
    echo [IMPORTANTE] Edita el archivo .env con tus datos de MySQL antes de continuar.
    echo              Abrilo con: notepad .env
    echo.
    pause
)

REM 6. Migraciones
echo [INFO] Ejecutando migraciones...
python manage.py migrate
echo [OK] Migraciones aplicadas.

REM 7. Cargar ciudades de Paraguay
echo [INFO] Cargando ciudades de Paraguay...
python manage.py loaddata apps/properties/fixtures/cities.json
echo [OK] Ciudades cargadas.

REM 8. Crear superusuario
echo.
echo [INFO] Creando superusuario para el panel admin...
python manage.py createsuperuser

REM 9. Collectstatic
echo [INFO] Recolectando archivos estaticos...
python manage.py collectstatic --noinput -v 0
echo [OK] Archivos estaticos listos.

echo.
echo ============================================================
echo   Setup completado!
echo   Ejecuta: python manage.py runserver
echo   Luego abre: http://127.0.0.1:8000
echo   Admin:     http://127.0.0.1:8000/admin
echo ============================================================
echo.
pause
