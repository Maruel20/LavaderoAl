from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, empleados, servicios, inventario, liquidaciones, convenios, tarifas, reportes, dashboard

app = FastAPI(title="Lavadero AL API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers que YA tienen "/api" en sus paths
app.include_router(auth.router)
app.include_router(empleados.router)
app.include_router(servicios.router)

# Estos routers también tienen "/api" en sus paths,
# así que NO se debe usar prefix="/api"
app.include_router(inventario.router)
app.include_router(liquidaciones.router)
app.include_router(convenios.router)
app.include_router(tarifas.router)
app.include_router(reportes.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "API del Lavadero funcionando correctamente 🚀"}
