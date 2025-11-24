# Guía de Instalación - Lavadero AL

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior**
- **Node.js 16 o superior**
- **MySQL 8.0 o superior**
- **npm o yarn**
- **Git** (opcional)

## 🚀 Instalación Paso a Paso

### 1. Clonar o Descargar el Proyecto

```bash
git clone <url-del-repositorio>
cd LavaderoAl
```

### 2. Configurar la Base de Datos

#### 2.1 Iniciar MySQL
```bash
# En Windows con XAMPP
# Inicia XAMPP y activa MySQL

# En Linux/Mac
sudo service mysql start
# o
sudo systemctl start mysql
```

#### 2.2 Crear la Base de Datos
```bash
mysql -u root -p < backend/schema.sql
```

O manualmente:
```bash
mysql -u root -p
# Dentro de MySQL:
source backend/schema.sql;
exit;
```

### 3. Configurar el Backend

#### 3.1 Crear Entorno Virtual
```bash
cd backend
python -m venv venv
```

#### 3.2 Activar Entorno Virtual
```bash
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

#### 3.3 Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 3.4 Configurar Variables de Entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env  # o usa tu editor favorito
```

Contenido mínimo de `.env`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=lavadero_al
DB_PORT=3306

ENV=development

# IMPORTANTE: Genera una clave segura con:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=tu_clave_secreta_aqui
```

#### 3.5 Hashear Contraseñas (IMPORTANTE)
Las contraseñas de prueba en `schema.sql` están en texto plano. Debes hashearlas:

```bash
python migrate_passwords.py
```

Esto convertirá:
- `admin` / `admin123` → Contraseña hasheada con bcrypt
- `empleado1` / `emp123` → Contraseña hasheada con bcrypt

**Nota:** Las credenciales de login siguen siendo las mismas, pero ahora están seguras.

#### 3.6 Iniciar el Servidor Backend
```bash
# Opción 1: Usando el script
./start_server.sh          # Linux/Mac
start_server.bat           # Windows

# Opción 2: Manualmente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

### 4. Configurar el Frontend

#### 4.1 Instalar Dependencias
```bash
cd ../  # Volver a la raíz del proyecto
npm install
```

#### 4.2 Iniciar el Servidor de Desarrollo
```bash
npm run dev
```

El frontend estará disponible en:
- http://localhost:5173

## ✅ Verificación de Instalación

### 1. Verificar Backend
Abre http://localhost:8000/docs y deberías ver la documentación de Swagger.

### 2. Verificar Frontend
Abre http://localhost:5173 y deberías ver la página de login.

### 3. Probar Login
```
Usuario: admin
Contraseña: admin123
```

## 🔧 Solución de Problemas Comunes

### Error: "No module named 'fastapi'"
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Access denied for user"
```bash
# Verifica tus credenciales en backend/.env
# Asegúrate de que MySQL esté corriendo
mysql -u root -p  # Prueba conectarte manualmente
```

### Error: "Database 'lavadero_al' doesn't exist"
```bash
# Crea la base de datos nuevamente
mysql -u root -p < backend/schema.sql
```

### Error: "Token inválido" al hacer login
```bash
# Asegúrate de haber ejecutado migrate_passwords.py
cd backend
python migrate_passwords.py
```

### Error: CORS en el Frontend
Verifica que el backend permita el origen correcto en `backend/main.py`:
```python
origins = [
    "http://localhost:5173",  # Puerto de Vite
    "http://127.0.0.1:5173",
]
```

## 📝 Usuarios de Prueba

Después de ejecutar `migrate_passwords.py`:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | admin |
| empleado1 | emp123 | empleado |

## 🔐 Seguridad Post-Instalación

1. **Cambiar SECRET_KEY**: Genera una nueva clave segura
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Cambiar contraseñas de prueba**: No uses admin/admin123 en producción

3. **Configurar HTTPS**: En producción, usa siempre HTTPS

4. **Backup regular**: Haz backup de la base de datos regularmente
```bash
mysqldump -u root -p lavadero_al > backup_$(date +%Y%m%d).sql
```

## 📚 Siguientes Pasos

- Lee [README.md](README.md) para conocer las características
- Explora la documentación API en http://localhost:8000/docs
- Revisa las configuraciones en `backend/.env`
- Personaliza las tarifas en la sección "Tarifas"

## 🆘 Soporte

Si tienes problemas:
1. Revisa esta guía nuevamente
2. Verifica los logs del backend y frontend
3. Consulta la documentación de FastAPI y Vue
4. Abre un issue en el repositorio del proyecto

---

**¡Instalación completada!** 🎉

Ahora puedes comenzar a usar el sistema de gestión de Lavadero AL.
