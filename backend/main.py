from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, empleados, servicios, inventario, liquidaciones, convenios, tarifas, reportes, dashboard

app = FastAPI(title="Lavadero AL API")

# --- CONFIGURACIÓN CORS ---
# Permite que tu Frontend Vue (puerto 5173) hable con este Backend (puerto 8000/5000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pon ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUIR RUTAS ---
app.include_router(auth.router)
app.include_router(empleados.router)
app.include_router(servicios.router)
app.include_router(inventario.router)
app.include_router(liquidaciones.router)
app.include_router(convenios.router)
app.include_router(tarifas.router)
app.include_router(reportes.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "API del Lavadero funcionando correctamente 🚀"}

# Para ejecutar: uvicorn main:app --reload --port 8000