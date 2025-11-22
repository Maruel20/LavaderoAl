<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-speedometer2 me-2"></i>
          Dashboard
        </h2>
        <p class="text-muted">Resumen general del lavadero</p>
      </div>
    </div>

     Métricas principales 
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="metric-card blue">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <div class="metric-label">Servicios Hoy</div>
              <div class="metric-value">{{ metrics.serviciosHoy }}</div>
            </div>
            <i class="bi bi-water" style="font-size: 3rem; opacity: 0.3;"></i>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="metric-card green">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <div class="metric-label">Ingresos Hoy</div>
              <div class="metric-value">${{ metrics.ingresosHoy.toLocaleString() }}</div>
            </div>
            <i class="bi bi-cash-stack" style="font-size: 3rem; opacity: 0.3;"></i>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="metric-card orange">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <div class="metric-label">Clientes Activos</div>
              <div class="metric-value">{{ metrics.clientesActivos }}</div>
            </div>
            <i class="bi bi-people" style="font-size: 3rem; opacity: 0.3;"></i>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="metric-card red">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <div class="metric-label">Insumos Bajos</div>
              <div class="metric-value">{{ metrics.insumosBajos }}</div>
            </div>
            <i class="bi bi-exclamation-triangle" style="font-size: 3rem; opacity: 0.3;"></i>
          </div>
        </div>
      </div>
    </div>

     Servicios recientes y alertas 
    <div class="row g-3">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="bi bi-clock-history me-2"></i>
              Servicios Recientes
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Cliente</th>
                    <th>Vehículo</th>
                    <th>Servicio</th>
                    <th>Empleado</th>
                    <th>Monto</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="servicio in serviciosRecientes" :key="servicio.id">
                    <td>#{{ servicio.id }}</td>
                    <td>{{ servicio.cliente }}</td>
                    <td>{{ servicio.vehiculo }}</td>
                    <td>{{ servicio.tipoServicio }}</td>
                    <td>{{ servicio.empleado }}</td>
                    <td class="fw-bold">${{ servicio.monto.toLocaleString() }}</td>
                    <td>
                      <span :class="'badge bg-' + servicio.estadoColor">
                        {{ servicio.estado }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
         Alertas de inventario 
        <div class="card mb-3">
          <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Alertas de Inventario
            </h5>
          </div>
          <div class="card-body">
            <div class="list-group list-group-flush">
              <div 
                v-for="alerta in alertasInventario" 
                :key="alerta.id"
                class="list-group-item px-0"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ alerta.nombre }}</strong>
                    <br>
                    <small class="text-muted">Stock: {{ alerta.stock }} {{ alerta.unidad }}</small>
                  </div>
                  <span class="badge bg-danger">Bajo</span>
                </div>
              </div>
            </div>
          </div>
        </div>

         Empleados activos 
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">
              <i class="bi bi-person-check me-2"></i>
              Empleados Activos
            </h5>
          </div>
          <div class="card-body">
            <div class="list-group list-group-flush">
              <div 
                v-for="empleado in empleadosActivos" 
                :key="empleado.id"
                class="list-group-item px-0"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <span class="status-icon active"></span>
                    <strong>{{ empleado.nombre }}</strong>
                    <br>
                    <small class="text-muted">{{ empleado.serviciosHoy }} servicios hoy</small>
                  </div>
                  <span class="badge bg-success">${{ empleado.comisionHoy.toLocaleString() }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return {
      metrics: {
        serviciosHoy: 24,
        ingresosHoy: 450000,
        clientesActivos: 156,
        insumosBajos: 3
      },
      serviciosRecientes: [
        {
          id: 1,
          cliente: 'Juan Pérez',
          vehiculo: 'Toyota Corolla ABC123',
          tipoServicio: 'Lavado Completo',
          empleado: 'Carlos Gómez',
          monto: 25000,
          estado: 'Completado',
          estadoColor: 'success'
        },
        {
          id: 2,
          cliente: 'María López',
          vehiculo: 'Honda Civic XYZ789',
          tipoServicio: 'Lavado Express',
          empleado: 'Ana Martínez',
          monto: 15000,
          estado: 'En Proceso',
          estadoColor: 'warning'
        },
        {
          id: 3,
          cliente: 'Pedro Ramírez',
          vehiculo: 'Chevrolet Spark DEF456',
          tipoServicio: 'Encerado',
          empleado: 'Luis Torres',
          monto: 35000,
          estado: 'Completado',
          estadoColor: 'success'
        }
      ],
      alertasInventario: [
        { id: 1, nombre: 'Shampoo Premium', stock: 2, unidad: 'L' },
        { id: 2, nombre: 'Cera Líquida', stock: 1, unidad: 'L' },
        { id: 3, nombre: 'Toallas Microfibra', stock: 5, unidad: 'unidades' }
      ],
      empleadosActivos: [
        { id: 1, nombre: 'Carlos Gómez', serviciosHoy: 8, comisionHoy: 80000 },
        { id: 2, nombre: 'Ana Martínez', serviciosHoy: 6, comisionHoy: 60000 },
        { id: 3, nombre: 'Luis Torres', serviciosHoy: 5, comisionHoy: 55000 }
      ]
    }
  }
}
</script>

