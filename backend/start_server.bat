@echo off
REM Script para iniciar el servidor de desarrollo del Lavadero AL en Windows

echo ==========================================
echo    Iniciando Servidor Lavadero AL API
echo ==========================================
echo.

REM Verificar si el entorno virtual existe
if not exist "venv\" (
    echo Error: No se encontro el entorno virtual.
    echo Por favor, crea el entorno virtual primero:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar que las dependencias estan instaladas
echo Verificando dependencias...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Iniciando servidor en http://localhost:8000
echo Documentacion API disponible en: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar el servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
