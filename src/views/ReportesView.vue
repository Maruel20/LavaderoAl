<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-graph-up me-2"></i>
          
        </h2>
        <p class="text-muted">Analiza el rendimiento del lavadero</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-success">
          <i class="bi bi-file-earmark-excel me-2"></i>
          Exportar Reporte
        </button>
      </div>
    </div>
 
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
            <label class="form-label">Tipo de Reporte</label>
            <select class="form-select" v-model="tipoReporte">
              <option value="general">General</option>
              <option value="financiero">Financiero</option>
              <option value="empleados">Por Empleado</option>
              <option value="servicios">Por Servicio</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Fecha Inicio</label>
            <input type="date" class="form-control" v-model="fechaInicio">
          </div>
          <div class="col-md-3">
            <label class="form-label">Fecha Fin</label>
            <input type="date" class="form-control" v-model="fechaFin">
          </div>
          <div class="col-md-3">
            <label class="form-label">&nbsp;</label>
            <button class="btn btn-primary w-100">
              <i class="bi bi-search me-2"></i>
              Generar Reporte
            </button>
          </div>
        </div>
      </div>
    </div>

     
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-primary">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Ingresos Totales</h6>
                <h3 class="mb-0">${{ metricas.ingresosTotales.toLocaleString() }}</h3>
                <small class="text-success">
                  <i class="bi bi-arrow-up"></i> +12% vs mes anterior
                </small>
              </div>
              <i class="bi bi-cash-stack text-primary" style="font-size: 2.5rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Total Servicios</h6>
                <h3 class="mb-0">{{ metricas.totalServicios }}</h3>
                <small class="text-success">
                  <i class="bi bi-arrow-up"></i> +8% vs mes anterior
                </small>
              </div>
              <i class="bi bi-water text-success" style="font-size: 2.5rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Ticket Promedio</h6>
                <h3 class="mb-0">${{ metricas.ticketPromedio.toLocaleString() }}</h3>
                <small class="text-success">
                  <i class="bi bi-arrow-up"></i> +5% vs mes anterior
                </small>
              </div>
              <i class="bi bi-receipt text-warning" style="font-size: 2.5rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-info">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Clientes Atendidos</h6>
                <h3 class="mb-0">{{ metricas.clientesAtendidos }}</h3>
                <small class="text-success">
                  <i class="bi bi-arrow-up"></i> +15% vs mes anterior
                </small>
              </div>
              <i class="bi bi-people text-info" style="font-size: 2.5rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

     
    <div class="row g-3">
       
      <div class="col-lg-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="bi bi-pie-chart me-2"></i>
              Servicios por Tipo
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Tipo de Servicio</th>
                    <th>Cantidad</th>
                    <th>Ingresos</th>
                    <th>%</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="servicio in serviciosPorTipo" :key="servicio.tipo">
                    <td>{{ servicio.tipo }}</td>
                    <td>
                      <span class="badge bg-primary">{{ servicio.cantidad }}</span>
                    </td>
                    <td class="fw-bold">${{ servicio.ingresos.toLocaleString() }}</td>
                    <td>
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar" 
                          :style="{ width: servicio.porcentaje + '%' }"
                        >
                          {{ servicio.porcentaje }}%
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

     
      <div class="col-lg-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="bi bi-person-badge me-2"></i>
              Rendimiento por Empleado
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Empleado</th>
                    <th>Servicios</th>
                    <th>Ingresos</th>
                    <th>Comisión</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="empleado in rendimientoEmpleados" :key="empleado.nombre">
                    <td>
                      <strong>{{ empleado.nombre }}</strong>
                    </td>
                    <td>
                      <span class="badge bg-info">{{ empleado.servicios }}</span>
                    </td>
                    <td class="fw-bold">${{ empleado.ingresos.toLocaleString() }}</td>
                    <td class="text-success fw-bold">${{ empleado.comision.toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

    
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="bi bi-bar-chart me-2"></i>
              Ingresos Diarios (Últimos 7 días)
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Servicios</th>
                    <th>Ingresos</th>
                    <th>Comisiones</th>
                    <th>Ganancia Neta</th>
                    <th>Gráfico</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="dia in ingresosDiarios" :key="dia.fecha">
                    <td>{{ dia.fecha }}</td>
                    <td>
                      <span class="badge bg-primary">{{ dia.servicios }}</span>
                    </td>
                    <td class="fw-bold">${{ dia.ingresos.toLocaleString() }}</td>
                    <td class="text-warning">${{ dia.comisiones.toLocaleString() }}</td>
                    <td class="text-success fw-bold">${{ dia.gananciaNeta.toLocaleString() }}</td>
                    <td>
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar bg-success" 
                          :style="{ width: (dia.ingresos / 500000 * 100) + '%' }"
                        >
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReportesView',
  data() {
    return {
      tipoReporte: 'general',
      fechaInicio: '',
      fechaFin: '',
      metricas: {
        ingresosTotales: 3450000,
        totalServicios: 156,
        ticketPromedio: 22115,
        clientesAtendidos: 89
      },
      serviciosPorTipo: [
        { tipo: 'Lavado Completo', cantidad: 65, ingresos: 1625000, porcentaje: 47 },
        { tipo: 'Lavado Express', cantidad: 48, ingresos: 720000, porcentaje: 21 },
        { tipo: 'Encerado', cantidad: 28, ingresos: 980000, porcentaje: 28 },
        { tipo: 'Pulido', cantidad: 15, ingresos: 675000, porcentaje: 20 }
      ],
      rendimientoEmpleados: [
        { nombre: 'Carlos Gómez', servicios: 58, ingresos: 1450000, comision: 580000 },
        { nombre: 'Ana Martínez', servicios: 52, ingresos: 1300000, comision: 520000 },
        { nombre: 'Luis Torres', servicios: 46, ingresos: 1150000, comision: 575000 }
      ],
      ingresosDiarios: [
        { fecha: '04/01/2025', servicios: 18, ingresos: 450000, comisiones: 180000, gananciaNeta: 270000 },
        { fecha: '05/01/2025', servicios: 22, ingresos: 550000, comisiones: 220000, gananciaNeta: 330000 },
        { fecha: '06/01/2025', servicios: 25, ingresos: 625000, comisiones: 250000, gananciaNeta: 375000 },
        { fecha: '07/01/2025', servicios: 20, ingresos: 500000, comisiones: 200000, gananciaNeta: 300000 },
        { fecha: '08/01/2025', servicios: 24, ingresos: 600000, comisiones: 240000, gananciaNeta: 360000 },
        { fecha: '09/01/2025', servicios: 23, ingresos: 575000, comisiones: 230000, gananciaNeta: 345000 },
        { fecha: '10/01/2025', servicios: 24, ingresos: 600000, comisiones: 240000, gananciaNeta: 360000 }
      ]
    }
  }
}
</script>
