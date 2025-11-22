<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-file-earmark-text me-2"></i>
          Gestión de Convenios
        </h2>
        <p class="text-muted">Administra convenios con empresas, clientes y sus vehículos</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalConvenio">
          <i class="bi bi-plus-circle me-2"></i>
          Nuevo Convenio
        </button>
      </div>
    </div>

     Estadísticas de convenios 
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-primary">
          <div class="card-body">
            <h6 class="text-muted mb-1">Total Convenios</h6>
            <h3 class="mb-0">{{ convenios.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-success">
          <div class="card-body">
            <h6 class="text-muted mb-1">Activos</h6>
            <h3 class="mb-0 text-success">{{ conveniosActivos }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-info">
          <div class="card-body">
            <h6 class="text-muted mb-1">Vehículos en Convenio</h6>
            <h3 class="mb-0 text-info">{{ totalVehiculosConvenio }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-warning">
          <div class="card-body">
            <h6 class="text-muted mb-1">Ingresos Mensuales</h6>
            <h3 class="mb-0 text-warning">${{ ingresosMensualesConvenios.toLocaleString() }}</h3>
          </div>
        </div>
      </div>
    </div>

     Filtros 
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Buscar convenio..."
              v-model="busqueda"
            >
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroEstado">
              <option value="">Todos los estados</option>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
              <option value="vencido">Vencido</option>
            </select>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroTipo">
              <option value="">Todos los tipos</option>
              <option value="mensual">Mensual</option>
              <option value="anual">Anual</option>
            </select>
          </div>
        </div>
      </div>
    </div>

     Tabla de convenios 
    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Cliente/Empresa</th>
                <th>RUT</th>
                <th>Contacto</th>
                <th>Tipo</th>
                <th>Vigencia</th>
                <th>Vehículos</th>
                <th>Descuento</th>
                <th>Valor Mensual</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="convenio in convenios" :key="convenio.id">
                <td>#{{ convenio.id }}</td>
                <td>
                  <strong>{{ convenio.cliente }}</strong>
                </td>
                <td>{{ convenio.rut }}</td>
                <td>
                  <small>{{ convenio.telefono }}</small><br>
                  <small class="text-muted">{{ convenio.email }}</small>
                </td>
                <td>
                  <span :class="'badge bg-' + convenio.tipoColor">
                    {{ convenio.tipo }}
                  </span>
                </td>
                <td>
                  <small>{{ convenio.fechaInicio }}</small><br>
                  <small class="text-muted">{{ convenio.fechaFin }}</small>
                </td>
                <td>
                  <button 
                    class="badge bg-info border-0" 
                    data-bs-toggle="modal" 
                    data-bs-target="#modalVehiculos"
                    @click="verVehiculos(convenio)"
                  >
                    {{ convenio.vehiculos }} <i class="bi bi-eye ms-1"></i>
                  </button>
                </td>
                <td>
                  <span class="badge bg-success">{{ convenio.descuento }}%</span>
                </td>
                <td class="fw-bold">${{ convenio.valorMensual.toLocaleString() }}</td>
                <td>
                  <span :class="'badge bg-' + convenio.estadoColor">
                    {{ convenio.estado }}
                  </span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button 
                      class="btn btn-outline-warning" 
                      title="Editar"
                      data-bs-toggle="modal" 
                      data-bs-target="#modalConvenio"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-secondary" title="Renovar">
                      <i class="bi bi-arrow-repeat"></i>
                    </button>
                    <button class="btn btn-outline-danger" title="Desactivar">
                      <i class="bi bi-x-circle"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

     Modal para nuevo/editar convenio 
    <div class="modal fade" id="modalConvenio" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-file-earmark-text me-2"></i>
              Nuevo Convenio
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form>
               Datos del Cliente/Empresa 
              <h6 class="fw-bold mb-3">
                <i class="bi bi-building me-2"></i>
                Datos del Cliente/Empresa
              </h6>
              <div class="row g-3 mb-4">
                <div class="col-md-6">
                  <label class="form-label">Nombre/Razón Social *</label>
                  <input type="text" class="form-control" placeholder="Ej: Transportes Rápidos S.A." required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">RUT *</label>
                  <input type="text" class="form-control" placeholder="76.543.210-K" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Teléfono *</label>
                  <input type="tel" class="form-control" placeholder="+56 2 2345 6789" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Email *</label>
                  <input type="email" class="form-control" placeholder="contacto@empresa.cl" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Dirección</label>
                  <input type="text" class="form-control" placeholder="Av. Principal 123">
                </div>
              </div>

               Datos del Convenio 
              <h6 class="fw-bold mb-3">
                <i class="bi bi-file-text me-2"></i>
                Datos del Convenio
              </h6>
              <div class="row g-3 mb-4">
                <div class="col-md-3">
                  <label class="form-label">Tipo de Convenio *</label>
                  <select class="form-select" required>
                    <option value="">Seleccionar...</option>
                    <option value="mensual">Mensual</option>
                    <option value="anual">Anual</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Fecha de Inicio *</label>
                  <input type="date" class="form-control" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Fecha de Fin *</label>
                  <input type="date" class="form-control" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Descuento (%) *</label>
                  <input type="number" class="form-control" min="0" max="100" placeholder="20" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Valor Mensual *</label>
                  <input type="number" class="form-control" placeholder="300000" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Servicios Incluidos/Mes *</label>
                  <input type="number" class="form-control" placeholder="4" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Comisión Empleado (%) *</label>
                  <select class="form-select" required>
                    <option value="">Seleccionar...</option>
                    <option value="40">40% (Normal)</option>
                    <option value="50">50% (Convenio)</option>
                  </select>
                </div>
              </div>

               Vehículos del Convenio 
              <h6 class="fw-bold mb-3">
                <i class="bi bi-car-front me-2"></i>
                Vehículos del Convenio
                <button type="button" class="btn btn-sm btn-success ms-2" @click="agregarVehiculo">
                  <i class="bi bi-plus-circle"></i> Agregar Vehículo
                </button>
              </h6>
              <div class="table-responsive mb-3">
                <table class="table table-sm table-bordered">
                  <thead>
                    <tr>
                      <th>Patente</th>
                      <th>Marca</th>
                      <th>Modelo</th>
                      <th>Año</th>
                      <th>Tipo</th>
                      <th>Color</th>
                      <th>Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(vehiculo, index) in vehiculosTemp" :key="index">
                      <td><input type="text" class="form-control form-control-sm" v-model="vehiculo.patente" placeholder="ABC123"></td>
                      <td><input type="text" class="form-control form-control-sm" v-model="vehiculo.marca" placeholder="Toyota"></td>
                      <td><input type="text" class="form-control form-control-sm" v-model="vehiculo.modelo" placeholder="Corolla"></td>
                      <td><input type="number" class="form-control form-control-sm" v-model="vehiculo.año" placeholder="2020"></td>
                      <td>
                        <select class="form-select form-select-sm" v-model="vehiculo.tipo">
                          <option value="">Tipo...</option>
                          <option value="auto">Auto</option>
                          <option value="camioneta">Camioneta</option>
                          <option value="camion">Camión</option>
                          <option value="moto">Moto</option>
                        </select>
                      </td>
                      <td><input type="text" class="form-control form-control-sm" v-model="vehiculo.color" placeholder="Blanco"></td>
                      <td>
                        <button type="button" class="btn btn-sm btn-danger" @click="eliminarVehiculo(index)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="col-12">
                <label class="form-label">Términos y Condiciones</label>
                <textarea class="form-control" rows="3" placeholder="Detalles adicionales del convenio..."></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary">
              <i class="bi bi-save me-2"></i>
              Guardar Convenio
            </button>
          </div>
        </div>
      </div>
    </div>

     Modal para ver vehículos del convenio 
    <div class="modal fade" id="modalVehiculos" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-car-front me-2"></i>
              Vehículos del Convenio
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Patente</th>
                    <th>Marca</th>
                    <th>Modelo</th>
                    <th>Año</th>
                    <th>Tipo</th>
                    <th>Color</th>
                    <th>Servicios</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="vehiculo in vehiculosSeleccionados" :key="vehiculo.id">
                    <td><strong>{{ vehiculo.patente }}</strong></td>
                    <td>{{ vehiculo.marca }}</td>
                    <td>{{ vehiculo.modelo }}</td>
                    <td>{{ vehiculo.año }}</td>
                    <td><span class="badge bg-primary">{{ vehiculo.tipo }}</span></td>
                    <td>{{ vehiculo.color }}</td>
                    <td><span class="badge bg-info">{{ vehiculo.servicios }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConveniosView',
  data() {
    return {
      busqueda: '',
      filtroEstado: '',
      filtroTipo: '',
      vehiculosTemp: [
        { patente: '', marca: '', modelo: '', año: '', tipo: '', color: '' }
      ],
      vehiculosSeleccionados: [],
      convenios: [
        {
          id: 1,
          cliente: 'Transportes Rápidos S.A.',
          rut: '76.543.210-K',
          telefono: '+56 2 2345 6789',
          email: 'contacto@transportes.cl',
          tipo: 'Anual',
          tipoColor: 'primary',
          fechaInicio: '01/01/2025',
          fechaFin: '31/12/2025',
          vehiculos: 15,
          descuento: 20,
          valorMensual: 300000,
          estado: 'Activo',
          estadoColor: 'success',
          listaVehiculos: [
            { id: 1, patente: 'ABC123', marca: 'Toyota', modelo: 'Corolla', año: 2020, tipo: 'Auto', color: 'Blanco', servicios: 12 },
            { id: 2, patente: 'DEF456', marca: 'Honda', modelo: 'Civic', año: 2019, tipo: 'Auto', color: 'Negro', servicios: 10 }
          ]
        },
        {
          id: 2,
          cliente: 'Logística Express Ltda.',
          rut: '77.123.456-7',
          telefono: '+56 2 3456 7890',
          email: 'info@logistica.cl',
          tipo: 'Mensual',
          tipoColor: 'info',
          fechaInicio: '01/01/2025',
          fechaFin: '31/01/2025',
          vehiculos: 8,
          descuento: 15,
          valorMensual: 150000,
          estado: 'Activo',
          estadoColor: 'success',
          listaVehiculos: [
            { id: 3, patente: 'GHI789', marca: 'Chevrolet', modelo: 'Spark', año: 2021, tipo: 'Auto', color: 'Rojo', servicios: 8 }
          ]
        },
        {
          id: 3,
          cliente: 'Distribuidora del Sur',
          rut: '78.987.654-3',
          telefono: '+56 2 4567 8901',
          email: 'ventas@distribuidora.cl',
          tipo: 'Anual',
          tipoColor: 'primary',
          fechaInicio: '01/06/2024',
          fechaFin: '31/05/2025',
          vehiculos: 20,
          descuento: 25,
          valorMensual: 450000,
          estado: 'Activo',
          estadoColor: 'success',
          listaVehiculos: []
        }
      ]
    }
  },
  computed: {
    conveniosActivos() {
      return this.convenios.filter(c => c.estado === 'Activo').length
    },
    totalVehiculosConvenio() {
      return this.convenios.reduce((total, c) => total + c.vehiculos, 0)
    },
    ingresosMensualesConvenios() {
      return this.convenios
        .filter(c => c.estado === 'Activo')
        .reduce((total, c) => total + c.valorMensual, 0)
    }
  },
  methods: {
    agregarVehiculo() {
      this.vehiculosTemp.push({ patente: '', marca: '', modelo: '', año: '', tipo: '', color: '' })
    },
    eliminarVehiculo(index) {
      this.vehiculosTemp.splice(index, 1)
    },
    verVehiculos(convenio) {
      this.vehiculosSeleccionados = convenio.listaVehiculos
    }
  }
}
</script>
