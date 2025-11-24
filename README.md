# Lavadero AL - Sistema de Gestión

Sistema completo de gestión para lavadero de autos con control de servicios, empleados, inventario, liquidaciones, convenios y reportes.

## Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido para Python
- **MySQL** - Base de datos relacional
- **JWT** - Autenticación con tokens
- **Bcrypt** - Hash seguro de contraseñas
- **Pydantic** - Validación de datos

### Frontend
- **Vue 3** - Framework JavaScript progresivo
- **Vue Router** - Enrutamiento de páginas
- **Pinia** - Gestión de estado
- **Bootstrap 5** - Framework CSS
- **Axios** - Cliente HTTP

## Características Principales

✓ Autenticación con JWT
✓ Gestión de servicios de lavado
✓ Control de empleados y comisiones
✓ Sistema de inventario con alertas
✓ Liquidaciones de empleados
✓ Convenios con empresas
✓ Gestión de tarifas
✓ Dashboard con métricas
✓ Reportes detallados

## Instalación Rápida

### 1. Base de Datos
\`\`\`bash
mysql -u root -p < backend/schema.sql
\`\`\`

### 2. Backend
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env      # Editar con tus credenciales
./start_server.sh         # Linux/Mac
start_server.bat          # Windows
\`\`\`

### 3. Frontend
\`\`\`bash
npm install
npm run dev
\`\`\`

## Acceso al Sistema

- Frontend: http://localhost:5173
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

**Usuario de prueba:**
- Usuario: admin
- Contraseña: admin123

---

**Versión:** 1.0.0
