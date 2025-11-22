<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-cash-coin me-2"></i>
          Liquidaciones de Empleados
        </h2>
        <p class="text-muted">Gestiona las liquidaciones y comisiones</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalLiquidacion">
          <i class="bi bi-calculator me-2"></i>
          Nueva Liquidación
        </button>
      </div>
    </div>

    <!-- Filtros -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
            <label class="form-label">Mes</label>
            <select class="form-select" v-model="filtros.mes">
              <option value="">Todos los meses</option>
              <option value="1">Enero 2025</option>
              <option value="2">Febrero 2025</option>
              <option value="3">Marzo 2025</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Empleado</label>
            <select class="form-select" v-model="filtros.empleado">
              <option value="">Todos los empleados</option>
              <option value="1">Carlos Gómez</option>
              <option value="2">Ana Martínez</option>
              <option value="3">Luis Torres</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Estado</label>
            <select class="form-select" v-model="filtros.estado">
              <option value="">Todos los estados</option>
              <option value="pendiente">Pendiente</option>
              <option value="pagada">Pagada</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">&nbsp;</label>
            <button class="btn btn-success w-100">
              <i class="bi bi-file-earmark-excel me-2"></i>
              Exportar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Resumen de liquidaciones -->
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-primary">
          <div class="card-body">
            <h6 class="text-muted mb-1">Total Liquidaciones</h6>
            <h3 class="mb-0">{{ liquidaciones.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-warning">
          <div class="card-body">
            <h6 class="text-muted mb-1">Pendientes de Pago</h6>
            <h3 class="mb-0 text-warning">{{ liquidacionesPendientes }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-success">
          <div class="card-body">
            <h6 class="text-muted mb-1">Pagadas</h6>
            <h3 class="mb-0 text-success">{{ liquidacionesPagadas }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-info">
          <div class="card-body">
            <h6 class="text-muted mb-1">Total a Pagar</h6>
            <h3 class="mb-0 text-info">${{ totalAPagar.toLocaleString() }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla de liquidaciones -->
    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Empleado</th>
                <th>Período</th>
                <th>Servicios</th>
                <th>Total Servicios</th>
                <th>% Comisión</th>
                <th>Total Comisión</th>
                <th>Fecha Pago</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="liquidacion in liquidaciones" :key="liquidacion.id">
                <td>#{{ liquidacion.id }}</td>
                <td>
                  <strong>{{ liquidacion.empleado }}</strong>
                </td>
                <td>{{ liquidacion.periodo }}</td>
                <td>
                  <span class="badge bg-info">{{ liquidacion.cantidadServicios }}</span>
                </td>
                <td class="fw-bold">${{ liquidacion.totalServicios.toLocaleString() }}</td>
                <td>
                  <span class="badge bg-primary">{{ liquidacion.porcentajeComision }}%</span>
                </td>
                <td class="fw-bold text-success">${{ liquidacion.totalComision.toLocaleString() }}</td>
                <td>{{ liquidacion.fechaPago || '-' }}</td>
                <td>
                  <span :class="'badge bg-' + liquidacion.estadoColor">
                    {{ liquidacion.estado }}
                  </span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button 
                      class="btn btn-outline-primary" 
                      title="Ver detalles"
                      data-bs-toggle="modal" 
                      data-bs-target="#modalDetalleLiquidacion"
                      @click="verDetalle(liquidacion)"
                    >
                      <i class="bi bi-eye"></i>
                    </button>
                    <button 
                      v-if="liquidacion.estado === 'Pendiente'"
                      class="btn btn-outline-success" 
                      title="Marcar como pagada"
                      @click="marcarComoPagada(liquidacion)"
                    >
                      <i class="bi bi-check-circle"></i>
                    </button>
                    <button class="btn btn-outline-secondary" title="Imprimir">
                      <i class="bi bi-printer"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal para nueva liquidación -->
    <div class="modal fade" id="modalLiquidacion" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-calculator me-2"></i>
              Calcular Nueva Liquidación
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Empleado *</label>
                  <select class="form-select" required>
                    <option value="">Seleccionar empleado...</option>
                    <option value="1">Carlos Gómez</option>
                    <option value="2">Ana Martínez</option>
                    <option value="3">Luis Torres</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Período *</label>
                  <input type="month" class="form-control" required>
                </div>
                <div class="col-12">
                  <div class="alert alert-info">
                    <h6 class="alert-heading">Resumen del Período</h6>
                    <ul class="mb-0">
                      <li>Servicios realizados: <strong>45</strong></li>
                      <li>Total de servicios: <strong>$1.125.000</strong></li>
                      <li>Porcentaje de comisión: <strong>40%</strong></li>
                      <li>Total a liquidar: <strong class="text-success">$450.000</strong></li>
                    </ul>
                  </div>
                </div>
                <div class="col-12">
                  <label class="form-label">Observaciones</label>
                  <textarea class="form-control" rows="2"></textarea>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary">
              <i class="bi bi-save me-2"></i>
              Generar Liquidación
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para ver detalle de liquidación -->
    <div class="modal fade" id="modalDetalleLiquidacion" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-file-text me-2"></i>
              Detalle de Liquidación #{{ liquidacionSeleccionada.id }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <!-- Información del empleado -->
            <div class="card mb-3">
              <div class="card-body">
                <h6 class="card-title">Información del Empleado</h6>
                <div class="row">
                  <div class="col-md-6">
                    <p><strong>Nombre:</strong> {{ liquidacionSeleccionada.empleado }}</p>
                    <p><strong>Período:</strong> {{ liquidacionSeleccionada.periodo }}</p>
                  </div>
                  <div class="col-md-6">
                    <p><strong>Porcentaje Comisión:</strong> {{ liquidacionSeleccionada.porcentajeComision }}%</p>
                    <p><strong>Estado:</strong> 
                      <span :class="'badge bg-' + liquidacionSeleccionada.estadoColor">
                        {{ liquidacionSeleccionada.estado }}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Resumen financiero -->
            <div class="card mb-3">
              <div class="card-body">
                <h6 class="card-title">Resumen Financiero</h6>
                <div class="table-responsive">
                  <table class="table table-sm">
                    <tbody>
                      <tr>
                        <td><strong>Total de Servicios Realizados:</strong></td>
                        <td class="text-end">
                          <span class="badge bg-info">{{ liquidacionSeleccionada.cantidadServicios }}</span>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Monto Total de Servicios:</strong></td>
                        <td class="text-end fw-bold">${{ liquidacionSeleccionada.totalServicios?.toLocaleString() }}</td>
                      </tr>
                      <tr>
                        <td><strong>Porcentaje de Comisión:</strong></td>
                        <td class="text-end">
                          <span class="badge bg-primary">{{ liquidacionSeleccionada.porcentajeComision }}%</span>
                        </td>
                      </tr>
                      <tr class="table-success">
                        <td><strong>Total a Liquidar:</strong></td>
                        <td class="text-end fw-bold text-success fs-5">
                          ${{ liquidacionSeleccionada.totalComision?.toLocaleString() }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Detalle de servicios (ejemplo) -->
            <div class="card">
              <div class="card-body">
                <h6 class="card-title">Servicios Incluidos (Últimos 5)</h6>
                <div class="table-responsive">
                  <table class="table table-sm table-hover">
                    <thead>
                      <tr>
                        <th>Fecha</th>
                        <th>Tipo Servicio</th>
                        <th>Vehículo</th>
                        <th>Monto</th>
                        <th>Comisión</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>10/01/2025</td>
                        <td>Lavado Completo</td>
                        <td>Auto</td>
                        <td>$25,000</td>
                        <td class="text-success">$10,000</td>
                      </tr>
                      <tr>
                        <td>10/01/2025</td>
                        <td>Lavado Express</td>
                        <td>Moto</td>
                        <td>$15,000</td>
                        <td class="text-success">$6,000</td>
                      </tr>
                      <tr>
                        <td>09/01/2025</td>
                        <td>Lavado + Brillado</td>
                        <td>Camioneta</td>
                        <td>$35,000</td>
                        <td class="text-success">$14,000</td>
                      </tr>
                      <tr>
                        <td colspan="5" class="text-center text-muted">
                          <small>Mostrando últimos 5 servicios de {{ liquidacionSeleccionada.cantidadServicios }} totales</small>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cerrar
            </button>
            <button type="button" class="btn btn-primary">
              <i class="bi bi-printer me-2"></i>
              Imprimir
            </button>
            <button 
              v-if="liquidacionSeleccionada.estado === 'Pendiente'" 
              type="button" 
              class="btn btn-success"
              @click="marcarComoPagada(liquidacionSeleccionada)"
            >
              <i class="bi bi-check-circle me-2"></i>
              Marcar como Pagada
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LiquidacionesView',
  data() {
    return {
      filtros: {
        mes: '',
        empleado: '',
        estado: ''
      },
      liquidaciones: [
        {
          id: 1,
          empleado: 'Carlos Gómez',
          periodo: 'Enero 2025',
          cantidadServicios: 45,
          totalServicios: 1125000,
          porcentajeComision: 40,
          totalComision: 450000,
          fechaPago: '05/02/2025',
          estado: 'Pagada',
          estadoColor: 'success'
        },
        {
          id: 2,
          empleado: 'Ana Martínez',
          periodo: 'Enero 2025',
          cantidadServicios: 38,
          totalServicios: 950000,
          porcentajeComision: 40,
          totalComision: 380000,
          fechaPago: null,
          estado: 'Pendiente',
          estadoColor: 'warning'
        },
        {
          id: 3,
          empleado: 'Luis Torres',
          periodo: 'Enero 2025',
          cantidadServicios: 42,
          totalServicios: 1050000,
          porcentajeComision: 50,
          totalComision: 525000,
          fechaPago: null,
          estado: 'Pendiente',
          estadoColor: 'warning'
        }
      ],
      liquidacionSeleccionada: {}
    }
  },
  computed: {
    liquidacionesPendientes() {
      return this.liquidaciones.filter(l => l.estado === 'Pendiente').length
    },
    liquidacionesPagadas() {
      return this.liquidaciones.filter(l => l.estado === 'Pagada').length
    },
    totalAPagar() {
      return this.liquidaciones
        .filter(l => l.estado === 'Pendiente')
        .reduce((total, l) => total + l.totalComision, 0)
    }
  },
  methods: {
    verDetalle(liquidacion) {
      this.liquidacionSeleccionada = liquidacion
    },
    marcarComoPagada(liquidacion) {
      console.log('[v0] Marcando liquidación como pagada:', liquidacion.id)
      alert('Liquidación marcada como pagada correctamente')
    }
  }
}
</script>

