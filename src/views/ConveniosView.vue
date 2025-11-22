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
                      @click="editarConvenio(convenio)"
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
              {{ formularioConvenio.id ? 'Editar Convenio' : 'Nuevo Convenio' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="limpiarFormulario"></button>
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
                  <input type="text" class="form-control" placeholder="Ej: Transportes Rápidos S.A." v-model="formularioConvenio.nombre_empresa" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">RUT *</label>
                  <input type="text" class="form-control" placeholder="76.543.210-K" v-model="formularioConvenio.rut_empresa" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Contacto</label>
                  <input type="text" class="form-control" placeholder="Juan Pérez" v-model="formularioConvenio.contacto">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Teléfono *</label>
                  <input type="tel" class="form-control" placeholder="+56 2 2345 6789" v-model="formularioConvenio.telefono" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Email *</label>
                  <input type="email" class="form-control" placeholder="contacto@empresa.cl" v-model="formularioConvenio.email" required>
                </div>
                <div class="col-md-12">
                  <label class="form-label">Dirección</label>
                  <input type="text" class="form-control" placeholder="Av. Principal 123" v-model="formularioConvenio.direccion">
                </div>
              </div>

               Datos del Convenio 
              <h6 class="fw-bold mb-3">
                <i class="bi bi-file-text me-2"></i>
                Datos del Convenio
              </h6>
              <div class="row g-3 mb-4">
                <div class="col-md-3">
                  <label class="form-label">Tipo de Descuento *</label>
                  <select class="form-select" v-model="formularioConvenio.tipo_descuento" required>
                    <option value="">Seleccionar...</option>
                    <option value="porcentaje">Porcentaje</option>
                    <option value="monto">Monto Fijo</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Valor Descuento *</label>
                  <input type="number" class="form-control" min="0" placeholder="20" v-model="formularioConvenio.valor_descuento" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Fecha de Inicio *</label>
                  <input type="date" class="form-control" v-model="formularioConvenio.fecha_inicio" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Fecha de Término *</label>
                  <input type="date" class="form-control" v-model="formularioConvenio.fecha_termino" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Estado *</label>
                  <select class="form-select" v-model="formularioConvenio.estado" required>
                    <option value="activo">Activo</option>
                    <option value="inactivo">Inactivo</option>
                    <option value="vencido">Vencido</option>
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
                <label class="form-label">Observaciones</label>
                <textarea class="form-control" rows="3" placeholder="Detalles adicionales del convenio..." v-model="formularioConvenio.observaciones"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="limpiarFormulario">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary" @click="guardarConvenio" :disabled="cargando">
              <i class="bi bi-save me-2"></i>
              {{ cargando ? 'Guardando...' : 'Guardar Convenio' }}
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
import api from '@/services/api'

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
      convenios: [],
      formularioConvenio: {
        id: null,
        nombre_empresa: '',
        rut_empresa: '',
        contacto: '',
        telefono: '',
        email: '',
        direccion: '',
        tipo_descuento: 'porcentaje',
        valor_descuento: 0,
        estado: 'activo',
        fecha_inicio: '',
        fecha_termino: '',
        observaciones: ''
      },
      convenioSeleccionado: null,
      cargando: false
    }
  },
  computed: {
    conveniosActivos() {
      return this.convenios.filter(c => c.estado === 'activo').length
    },
    totalVehiculosConvenio() {
      return this.convenios.reduce((total, c) => total + (c.vehiculos || 0), 0)
    },
    ingresosMensualesConvenios() {
      return this.convenios
        .filter(c => c.estado === 'activo')
        .reduce((total, c) => total + (c.valorMensual || 0), 0)
    }
  },
  mounted() {
    this.cargarConvenios()
  },
  methods: {
    async cargarConvenios() {
      try {
        this.cargando = true
        const response = await api.getConvenios()
        this.convenios = response.data.map(convenio => ({
          ...convenio,
          cliente: convenio.nombre_empresa,
          rut: convenio.rut_empresa,
          tipo: convenio.tipo_descuento === 'porcentaje' ? 'Porcentaje' : 'Monto',
          tipoColor: convenio.tipo_descuento === 'porcentaje' ? 'primary' : 'info',
          fechaInicio: this.formatearFecha(convenio.fecha_inicio),
          fechaFin: this.formatearFecha(convenio.fecha_termino),
          descuento: convenio.valor_descuento,
          estadoColor: convenio.estado === 'activo' ? 'success' : 'danger',
          vehiculos: 0 // Se actualizará cuando se carguen los vehículos
        }))
      } catch (error) {
        console.error('Error al cargar convenios:', error)
        alert('Error al cargar los convenios. Por favor, intente nuevamente.')
      } finally {
        this.cargando = false
      }
    },

    async guardarConvenio() {
      try {
        this.cargando = true

        // Validar datos obligatorios
        if (!this.formularioConvenio.nombre_empresa || !this.formularioConvenio.rut_empresa ||
            !this.formularioConvenio.telefono || !this.formularioConvenio.email) {
          alert('Por favor, complete todos los campos obligatorios.')
          return
        }

        if (this.formularioConvenio.id) {
          // Actualizar convenio existente
          await api.updateConvenio(this.formularioConvenio.id, this.formularioConvenio)
          alert('Convenio actualizado exitosamente')
        } else {
          // Crear nuevo convenio
          const response = await api.createConvenio(this.formularioConvenio)

          // Si hay vehículos temporales, agregarlos al convenio
          if (this.vehiculosTemp.length > 0 && this.vehiculosTemp[0].patente) {
            const convenioId = response.data.id
            for (const vehiculo of this.vehiculosTemp) {
              if (vehiculo.patente) {
                await this.agregarVehiculoConvenio(convenioId, vehiculo)
              }
            }
          }

          alert('Convenio creado exitosamente')
        }

        // Recargar convenios
        await this.cargarConvenios()

        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalConvenio'))
        if (modal) modal.hide()

        // Limpiar formulario
        this.limpiarFormulario()
      } catch (error) {
        console.error('Error al guardar convenio:', error)
        alert('Error al guardar el convenio. Por favor, intente nuevamente.')
      } finally {
        this.cargando = false
      }
    },

    async agregarVehiculoConvenio(id_convenio, vehiculo) {
      try {
        const vehiculoData = {
          id_convenio: id_convenio,
          patente: vehiculo.patente,
          tipo_vehiculo: vehiculo.tipo,
          modelo: vehiculo.modelo,
          color: vehiculo.color
        }

        await api.addVehiculoConvenio(vehiculoData)
      } catch (error) {
        console.error('Error al agregar vehículo al convenio:', error)
        throw error
      }
    },

    async verVehiculos(convenio) {
      try {
        this.cargando = true
        this.convenioSeleccionado = convenio

        const response = await api.getVehiculosConvenio(convenio.id)
        this.vehiculosSeleccionados = response.data.map(vehiculo => ({
          ...vehiculo,
          tipo: vehiculo.tipo_vehiculo,
          servicios: vehiculo.servicios_realizados || 0
        }))
      } catch (error) {
        console.error('Error al cargar vehículos del convenio:', error)
        alert('Error al cargar los vehículos. Por favor, intente nuevamente.')
        this.vehiculosSeleccionados = []
      } finally {
        this.cargando = false
      }
    },

    agregarVehiculo() {
      this.vehiculosTemp.push({ patente: '', marca: '', modelo: '', año: '', tipo: '', color: '' })
    },

    eliminarVehiculo(index) {
      this.vehiculosTemp.splice(index, 1)
    },

    editarConvenio(convenio) {
      this.formularioConvenio = {
        id: convenio.id,
        nombre_empresa: convenio.nombre_empresa,
        rut_empresa: convenio.rut_empresa,
        contacto: convenio.contacto,
        telefono: convenio.telefono,
        email: convenio.email,
        direccion: convenio.direccion,
        tipo_descuento: convenio.tipo_descuento,
        valor_descuento: convenio.valor_descuento,
        estado: convenio.estado,
        fecha_inicio: convenio.fecha_inicio,
        fecha_termino: convenio.fecha_termino,
        observaciones: convenio.observaciones
      }
    },

    limpiarFormulario() {
      this.formularioConvenio = {
        id: null,
        nombre_empresa: '',
        rut_empresa: '',
        contacto: '',
        telefono: '',
        email: '',
        direccion: '',
        tipo_descuento: 'porcentaje',
        valor_descuento: 0,
        estado: 'activo',
        fecha_inicio: '',
        fecha_termino: '',
        observaciones: ''
      }
      this.vehiculosTemp = [
        { patente: '', marca: '', modelo: '', año: '', tipo: '', color: '' }
      ]
    },

    formatearFecha(fecha) {
      if (!fecha) return ''
      const date = new Date(fecha)
      const dia = String(date.getDate()).padStart(2, '0')
      const mes = String(date.getMonth() + 1).padStart(2, '0')
      const año = date.getFullYear()
      return `${dia}/${mes}/${año}`
    }
  }
}
</script>
