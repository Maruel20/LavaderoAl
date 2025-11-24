import { createRouter, createWebHistory } from "vue-router"
import LoginView from "../views/LoginView.vue"
import DashboardView from "../views/DashboardView.vue"
import ServiciosView from "../views/ServiciosView.vue"
import InventarioView from "../views/InventarioView.vue"
import EmpleadosView from "../views/EmpleadosView.vue"
import LiquidacionesView from "../views/LiquidacionesView.vue"
import ConveniosView from "../views/ConveniosView.vue"
import ReportesView from "../views/ReportesView.vue"
import TarifasView from "../views/TarifasView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/",
      name: "dashboard",
      component: DashboardView,
    },
    {
      path: "/servicios",
      name: "servicios",
      component: ServiciosView,
    },
    {
      path: "/inventario",
      name: "inventario",
      component: InventarioView,
    },
    {
      path: "/empleados",
      name: "empleados",
      component: EmpleadosView,
    },
    {
      path: "/liquidaciones",
      name: "liquidaciones",
      component: LiquidacionesView,
    },
    {
      path: "/convenios",
      name: "convenios",
      component: ConveniosView,
    },
    {
      path: "/reportes",
      name: "reportes",
      component: ReportesView,
    },
    {
      path: "/tarifas",
      name: "tarifas",
      component: TarifasView,
    },
  ],
})

// Protección de rutas con autenticación
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // Si no hay token y no va a login, redirigir a login
  if (!token && to.name !== 'login') {
    next({ name: 'login' })
  }
  // Si hay token y va a login, redirigir a dashboard
  else if (token && to.name === 'login') {
    next({ name: 'dashboard' })
  }
  // En cualquier otro caso, permitir navegación
  else {
    next()
  }
})

export default router
