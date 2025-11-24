<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-water me-2"></i>
          Gestión de Servicios
        </h2>
        <p class="text-muted">Registra y administra los servicios de lavado</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalServicio">
          <i class="bi bi-plus-circle me-2"></i>
          Nuevo Servicio
        </button>
      </div>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Fecha</th>
                <th>Patente</th>
                <th>Servicio</th>
                <th>Empleado</th>
                <th>Monto</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="servicios.length === 0">
                <td colspan="7" class="text-center py-5 text-muted">
                  <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                  No hay servicios registrados o no hay conexión con el servidor.
                </td>
              </tr>

              <tr v-for="servicio in servicios" :key="servicio.id">
                <td>#{{ servicio.id }}</td>
                <td>
                  {{ servicio.fecha }}<br>
                  <small class="text-muted">{{ servicio.hora }}</small>
                </td>
                <td class="fw-bold">{{ servicio.patente }}</td>
                <td>
                  <span class="badge bg-light text-dark border">
                    {{ servicio.tipoServicio }}
                  </span><br>
                  <small class="text-muted">{{ servicio.vehiculo }}</small>
                </td>
                <td>{{ servicio.empleado || 'Sin asignar' }}</td>
                <td class="fw-bold text-success">${{ servicio.monto?.toLocaleString() }}</td>
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

    <div class="modal fade" id="modalServicio" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-plus-circle me-2"></i>Registrar Nuevo Servicio
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="btnCerrarModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarServicio">
              
              <div class="row mb-4">
                <div class="col-12">
                  <div class="btn-group w-100" role="group">
                    <input type="radio" class="btn-check" name="tipoRegistro" id="servicioNormal" value="normal" v-model="tipoRegistro">
                    <label class="btn btn-outline-primary" for="servicioNormal">Servicio Normal</label>
                    
                    <input type="radio" class="btn-check" name="tipoRegistro" id="servicioConvenio" value="convenio" v-model="tipoRegistro">
                    <label class="btn btn-outline-success" for="servicioConvenio">Servicio Convenio</label>
                  </div>
                </div>
              </div>

              <div v-if="tipoRegistro === 'normal'">
                <div class="row g-3">
                  <div class="col-md-4">
                    <label class="form-label fw-bold">Patente *</label>
                    <input type="text" class="form-control" v-model="patenteInput" placeholder="Ej: ABCD-10" required>
                  </div>

                  <div class="col-md-4">
                    <label class="form-label">Vehículo *</label>
                    <select class="form-select" v-model="tipoVehiculoSeleccionado" required @change="calcularPrecio">
                      <option value="">Seleccionar...</option>
                      <option value="auto">Auto</option>
                      <option value="camioneta">Camioneta</option>
                      <option value="suv">SUV</option>
                      <option value="furgon">Furgón</option>
                    </select>
                  </div>

                  <div class="col-md-4">
                    <label class="form-label">Servicio *</label>
                    <select class="form-select" v-model="tipoLavadoSeleccionado" required @change="calcularPrecio">
                      <option value="">Seleccionar...</option>
                      <option value="lavado_simple">Lavado Simple</option>
                      <option value="lavado_completo">Lavado Completo</option>
                      <option value="encerado">Encerado</option>
                      <option value="lavado_motor">Lavado de Motor</option>
                      <option value="pulido">Pulido</option>
                      <option value="descontaminacion">Descontaminación</option>
                    </select>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Empleado *</label>
                    <select class="form-select" v-model="empleadoSeleccionado" required>
                      <option value="">Seleccionar...</option>
                      <option v-for="emp in empleados" :key="emp.id" :value="emp.id">
                        {{ emp.nombre }}
                      </option>
                    </select>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Monto Total ($) *</label>
                    <input type="number" class="form-control" v-model="montoEditable" required>
                  </div>

                  <div class="col-12">
                    <div class="alert alert-info py-2 mb-0">
                      <small><i class="bi bi-info-circle me-1"></i> La comisión del empleado se calculará automáticamente.</small>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-else class="alert alert-warning">
                Funcionalidad de Convenios en desarrollo. Por favor use Servicio Normal por ahora.
              </div>

            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarServicio">
              <i class="bi bi-save me-2"></i> Guardar Servicio
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'; 

export default {
  name: 'ServiciosView',
  data() {
    return {
      // Datos de la base de datos
      servicios: [],
      empleados: [],

      // Formulario
      tipoRegistro: 'normal',
      patenteInput: '',
      tipoVehiculoSeleccionado: '',
      tipoLavadoSeleccionado: '',
      empleadoSeleccionado: '',
      montoEditable: 0,

      // Tarifas base - NOTA: Estas se cargarán dinámicamente desde la BD
      tarifas: {},
      tarifasOriginales: []
    }
  },
  mounted() {
    this.cargarDatos();
  },
  methods: {
    // 1. Cargar datos desde Python
    async cargarDatos() {
      try {
        // 1. Cargar Servicios
        const respuesta = await api.getServicios();

        // CORRECCIÓN: Verificamos si la respuesta viene directa o dentro de .data
        // Esto hace que funcione sin importar cómo esté configurado tu api.js
        const listaServicios = respuesta.data || respuesta;

        // Validación extra de seguridad: Si no es un array, lo forzamos a ser vacío
        if (!Array.isArray(listaServicios)) {
          console.error("El formato recibido no es una lista:", listaServicios);
          this.servicios = [];
          return;
        }

        this.servicios = listaServicios.map(s => ({
          id: s.id,
          fecha: new Date(s.fecha).toLocaleDateString(),
          hora: new Date(s.fecha).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
          patente: s.patente,
          vehiculo: this.formatearTipoVehiculo(s.tipo_vehiculo),
          tipoServicio: this.formatearTipoServicio(s.tipo_servicio),
          empleado: s.nombre_empleado,
          monto: s.monto_total,
          estado: s.estado,
          estadoColor: s.estado === 'pendiente' ? 'warning' : (s.estado === 'completado' ? 'success' : 'danger')
        }));

        // 2. Cargar Empleados
        const respuestaEmp = await api.getEmpleados();
        // Aplicamos la misma lógica de seguridad para empleados
        this.empleados = respuestaEmp.data || respuestaEmp;

        // 3. Cargar Tarifas dinámicamente desde la BD
        const respuestaTarifas = await api.getTarifas();
        this.tarifasOriginales = respuestaTarifas.data || respuestaTarifas;

        // Organizar tarifas en estructura fácil de usar
        this.tarifas = {};
        this.tarifasOriginales.forEach(tarifa => {
          if (!this.tarifas[tarifa.tipo_vehiculo]) {
            this.tarifas[tarifa.tipo_vehiculo] = {};
          }
          this.tarifas[tarifa.tipo_vehiculo][tarifa.tipo_servicio] = tarifa.precio;
        });

      } catch (error) {
        console.error("Error cargando datos:", error);
      }
    },

    // 2. Guardar en Python
    async guardarServicio() {
      // Validaciones simples
      if (!this.patenteInput || !this.empleadoSeleccionado || !this.tipoVehiculoSeleccionado) {
        alert("Por favor completa todos los campos obligatorios.");
        return;
      }

      // Preparar objeto para el backend
      const payload = {
        patente: this.patenteInput,
        tipo_vehiculo: this.tipoVehiculoSeleccionado,
        tipo_servicio: this.tipoLavadoSeleccionado,
        monto_total: parseInt(this.montoEditable),
        id_empleado: this.empleadoSeleccionado
      };

      try {
        await api.createServicio(payload);
        alert("¡Servicio registrado exitosamente!");
        
        // Recargar tabla
        await this.cargarDatos();
        
        // Limpiar formulario
        this.limpiarFormulario();
        
        // Cerrar modal (simulando clic en la X)
        document.getElementById('btnCerrarModal').click();

      } catch (error) {
        console.error(error);
        alert("Error al guardar. Verifica que el servidor Python esté corriendo.");
      }
    },

    // 3. Calcular precio sugerido desde tarifas dinámicas
    calcularPrecio() {
      if (this.tipoVehiculoSeleccionado && this.tipoLavadoSeleccionado) {
        const precio = this.tarifas[this.tipoVehiculoSeleccionado]?.[this.tipoLavadoSeleccionado] || 0;
        this.montoEditable = precio;
      }
    },

    // Formatear tipo de vehículo para mostrar
    formatearTipoVehiculo(tipo) {
      const formatos = {
        'auto': 'Auto',
        'camioneta': 'Camioneta',
        'suv': 'SUV',
        'furgon': 'Furgón'
      };
      return formatos[tipo] || tipo;
    },

    // Formatear tipo de servicio para mostrar
    formatearTipoServicio(tipo) {
      const formatos = {
        'lavado_simple': 'Lavado Simple',
        'lavado_completo': 'Lavado Completo',
        'encerado': 'Encerado',
        'lavado_motor': 'Lavado de Motor',
        'pulido': 'Pulido',
        'descontaminacion': 'Descontaminación'
      };
      return formatos[tipo] || tipo;
    },

    limpiarFormulario() {
      this.patenteInput = '';
      this.montoEditable = 0;
      this.tipoVehiculoSeleccionado = '';
      this.tipoLavadoSeleccionado = '';
      this.empleadoSeleccionado = '';
    }
  }
}
</script>