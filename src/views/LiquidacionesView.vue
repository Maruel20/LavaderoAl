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
              <option v-for="empleado in empleados" :key="empleado.id" :value="empleado.id">
                {{ empleado.nombre }}
              </option>
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
                  <select class="form-select" v-model="nuevaLiquidacion.id_empleado" required>
                    <option value="">Seleccionar empleado...</option>
                    <option v-for="empleado in empleados" :key="empleado.id" :value="empleado.id">
                      {{ empleado.nombre }} - {{ empleado.rut }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Fecha Inicio *</label>
                  <input type="date" class="form-control" v-model="nuevaLiquidacion.periodo_inicio" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Fecha Fin *</label>
                  <input type="date" class="form-control" v-model="nuevaLiquidacion.periodo_fin" required>
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
            <button type="button" class="btn btn-primary" @click="calcularLiquidacion">
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

            <!-- Detalle de servicios -->
            <div class="card">
              <div class="card-body">
                <h6 class="card-title">Servicios Incluidos</h6>
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
                      <tr v-if="liquidacionSeleccionada.servicios && liquidacionSeleccionada.servicios.length > 0"
                          v-for="servicio in liquidacionSeleccionada.servicios"
                          :key="servicio.id">
                        <td>{{ new Date(servicio.fecha).toLocaleDateString('es-CL') }}</td>
                        <td>{{ servicio.tipo_servicio }}</td>
                        <td>{{ servicio.tipo_vehiculo }}</td>
                        <td>${{ servicio.monto?.toLocaleString() }}</td>
                        <td class="text-success">${{ servicio.comision?.toLocaleString() }}</td>
                      </tr>
                      <tr v-else>
                        <td colspan="5" class="text-center text-muted">
                          <small>Cargando servicios...</small>
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
import api from '@/services/api'

export default {
  name: 'LiquidacionesView',
  data() {
    return {
      filtros: {
        mes: '',
        empleado: '',
        estado: ''
      },
      liquidaciones: [],
      empleados: [],
      nuevaLiquidacion: {
        id_empleado: '',
        periodo_inicio: '',
        periodo_fin: ''
      },
      liquidacionSeleccionada: {},
      detalleLiquidacion: null
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
  mounted() {
    this.cargarLiquidaciones()
    this.cargarEmpleados()
  },
  methods: {
    async cargarLiquidaciones() {
      try {
        const response = await api.getLiquidaciones()
        // Mapear los datos del backend al formato del frontend
        this.liquidaciones = response.map(liq => ({
          id: liq.id,
          empleado: liq.nombre_empleado,
          rut: liq.rut,
          periodo: `${liq.periodo_inicio} - ${liq.periodo_fin}`,
          cantidadServicios: liq.total_servicios,
          totalServicios: liq.monto_total_servicios,
          porcentajeComision: liq.porcentaje_comision,
          totalComision: liq.total_comisiones,
          fechaPago: liq.fecha_pago ? new Date(liq.fecha_pago).toLocaleDateString('es-CL') : null,
          estado: liq.estado === 'pendiente' ? 'Pendiente' : 'Pagada',
          estadoColor: liq.estado === 'pendiente' ? 'warning' : 'success',
          id_empleado: liq.id_empleado
        }))
        console.log('Liquidaciones cargadas:', this.liquidaciones.length)
      } catch (error) {
        console.error('Error al cargar liquidaciones:', error)
        alert('Error al cargar las liquidaciones: ' + (error.response?.data?.error || error.message))
      }
    },

    async cargarEmpleados() {
      try {
        this.empleados = await api.getEmpleados()
        console.log('Empleados cargados:', this.empleados.length)
      } catch (error) {
        console.error('Error al cargar empleados:', error)
        alert('Error al cargar los empleados: ' + (error.response?.data?.error || error.message))
      }
    },

    async calcularLiquidacion() {
      try {
        // Validar que todos los campos estén completos
        if (!this.nuevaLiquidacion.id_empleado || !this.nuevaLiquidacion.periodo_inicio || !this.nuevaLiquidacion.periodo_fin) {
          alert('Por favor complete todos los campos requeridos')
          return
        }

        // Llamar al API para calcular la liquidación
        const response = await api.calcularLiquidacion({
          periodo_inicio: this.nuevaLiquidacion.periodo_inicio,
          periodo_fin: this.nuevaLiquidacion.periodo_fin,
          id_empleado: this.nuevaLiquidacion.id_empleado
        })

        console.log('Liquidación calculada:', response)
        alert('Liquidación generada exitosamente')

        // Cerrar el modal
        const modal = document.getElementById('modalLiquidacion')
        const bootstrapModal = bootstrap.Modal.getInstance(modal)
        if (bootstrapModal) {
          bootstrapModal.hide()
        }

        // Limpiar el formulario
        this.nuevaLiquidacion = {
          id_empleado: '',
          periodo_inicio: '',
          periodo_fin: ''
        }

        // Recargar las liquidaciones
        await this.cargarLiquidaciones()
      } catch (error) {
        console.error('Error al calcular liquidación:', error)
        alert('Error al generar la liquidación: ' + (error.response?.data?.error || error.message))
      }
    },

    async marcarComoPagada(liquidacion) {
      try {
        if (!confirm('¿Está seguro de marcar esta liquidación como pagada?')) {
          return
        }

        await api.marcarLiquidacionPagada(liquidacion.id)
        console.log('Liquidación marcada como pagada:', liquidacion.id)
        alert('Liquidación marcada como pagada correctamente')

        // Cerrar el modal de detalle si está abierto
        const modal = document.getElementById('modalDetalleLiquidacion')
        const bootstrapModal = bootstrap.Modal.getInstance(modal)
        if (bootstrapModal) {
          bootstrapModal.hide()
        }

        // Recargar las liquidaciones
        await this.cargarLiquidaciones()
      } catch (error) {
        console.error('Error al marcar liquidación como pagada:', error)
        alert('Error al marcar la liquidación como pagada: ' + (error.response?.data?.error || error.message))
      }
    },

    async verDetalle(liquidacion) {
      try {
        this.liquidacionSeleccionada = liquidacion

        // Obtener el detalle completo de la liquidación
        this.detalleLiquidacion = await api.getLiquidacionDetalle(liquidacion.id)
        console.log('Detalle de liquidación:', this.detalleLiquidacion)

        // Actualizar los datos de la liquidación seleccionada con el detalle
        this.liquidacionSeleccionada = {
          ...liquidacion,
          servicios: this.detalleLiquidacion.servicios || []
        }
      } catch (error) {
        console.error('Error al cargar detalle de liquidación:', error)
        alert('Error al cargar el detalle de la liquidación: ' + (error.response?.data?.error || error.message))
        // Aún así mostrar el modal con la información básica
        this.liquidacionSeleccionada = liquidacion
      }
    }
  }
}
</script>

