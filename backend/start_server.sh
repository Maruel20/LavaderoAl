#!/bin/bash

# Script para iniciar el servidor de desarrollo del Lavadero AL

echo "=========================================="
echo "   Iniciando Servidor Lavadero AL API"
echo "=========================================="
echo ""

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "Error: No se encontró el entorno virtual."
    echo "Por favor, crea el entorno virtual primero:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate  # En Linux/Mac"
    echo "  venv\\Scripts\\activate     # En Windows"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual (Linux/Mac)
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Activando entorno virtual de Windows..."
    source venv/Scripts/activate
fi

# Verificar que las dependencias están instaladas
echo "Verificando dependencias..."
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

echo ""
echo "Iniciando servidor en http://localhost:8000"
echo "Documentación API disponible en: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar el servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
