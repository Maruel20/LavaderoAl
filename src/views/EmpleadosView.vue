<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-person-badge me-2"></i>
          Gestión de Empleados
        </h2>
        <p class="text-muted">Administra la información de tus empleados</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalEmpleado" @click="limpiarFormulario">
          <i class="bi bi-plus-circle me-2"></i>
          Nuevo Empleado
        </button>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Buscar por nombre o RUT..."
              v-model="busqueda"
            >
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroEstado">
              <option value="">Todos los estados</option>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
            </select>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroComision">
              <option value="">Todas las comisiones</option>
              <option value="40">40%</option>
              <option value="50">50%</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-primary">
          <div class="card-body">
            <h6 class="text-muted mb-1">Total Empleados</h6>
            <h3 class="mb-0">{{ empleados.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-success">
          <div class="card-body">
            <h6 class="text-muted mb-1">Activos</h6>
            <h3 class="mb-0 text-success">{{ empleadosActivos }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-info">
          <div class="card-body">
            <h6 class="text-muted mb-1">Servicios Hoy</h6>
            <h3 class="mb-0 text-info">{{ totalServiciosHoy }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-warning">
          <div class="card-body">
            <h6 class="text-muted mb-1">Comisiones Hoy</h6>
            <h3 class="mb-0 text-warning">${{ totalComisionesHoy.toLocaleString() }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>RUT</th>
                <th>Teléfono / Email</th>
                <th>% Comisión</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="empleados.length === 0">
                <td colspan="7" class="text-center py-4 text-muted">
                  No hay empleados registrados.
                </td>
              </tr>
              <tr v-for="empleado in empleadosFiltrados" :key="empleado.id">
                <td>#{{ empleado.id }}</td>
                <td>
                  <strong>{{ empleado.nombre }}</strong><br>
                  <small class="text-muted">Ingreso: {{ empleado.fechaIngreso || 'N/A' }}</small>
                </td>
                <td>{{ empleado.rut }}</td>
                <td>
                  <div><i class="bi bi-telephone-fill me-1 text-muted"></i> {{ empleado.telefono }}</div>
                  <div class="small text-muted"><i class="bi bi-envelope-fill me-1"></i> {{ empleado.email }}</div>
                </td>
                <td>
                  <span :class="'badge bg-' + (empleado.porcentajeComision == 50 ? 'success' : 'primary')">
                    {{ empleado.porcentajeComision }}%
                  </span>
                </td>
                <td>
                  <span :class="'badge bg-' + (empleado.estado === 'activo' ? 'success' : 'danger')">
                    {{ empleado.estado }}
                  </span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-warning" title="Editar">
                      <i class="bi bi-pencil"></i>
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

    <div class="modal fade" id="modalEmpleado" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-person-plus me-2"></i>
              {{ form.id ? 'Editar Empleado' : 'Nuevo Empleado' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" id="btnCerrarModalEmp"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarEmpleado">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Nombre Completo *</label>
                  <input type="text" class="form-control" v-model="form.nombre" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">RUT *</label>
                  <input type="text" class="form-control" v-model="form.rut" placeholder="12.345.678-9" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Teléfono *</label>
                  <input type="tel" class="form-control" v-model="form.telefono" placeholder="+56 9 1234 5678" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-control" v-model="form.email">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Porcentaje de Comisión *</label>
                  <select class="form-select" v-model="form.porcentaje_comision" required>
                    <option value="">Seleccionar...</option>
                    <option value="40">40% (Servicios normales)</option>
                    <option value="50">50% (Servicios con convenio)</option>
                  </select>
                </div>
                <div class="col-12">
                  <div class="alert alert-info mb-0">
                    <strong>Nota:</strong> Los empleados con convenio reciben 50% de comisión.
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary" @click="guardarEmpleado">
              <i class="bi bi-save me-2"></i>
              Guardar Empleado
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
  name: 'EmpleadosView',
  data() {
    return {
      // Filtros
      busqueda: '',
      filtroEstado: '',
      filtroComision: '',
      
      // Datos
      empleados: [],
      
      // Formulario
      form: {
        id: null,
        nombre: '',
        rut: '',
        telefono: '',
        email: '',
        porcentaje_comision: 40
      }
    }
  },
  mounted() {
    this.cargarEmpleados();
  },
  computed: {
    // Lógica de filtrado en el cliente (Frontend)
    empleadosFiltrados() {
      return this.empleados.filter(emp => {
        const coincideNombre = emp.nombre.toLowerCase().includes(this.busqueda.toLowerCase()) || 
                               emp.rut.toLowerCase().includes(this.busqueda.toLowerCase());
        const coincideEstado = this.filtroEstado ? emp.estado === this.filtroEstado : true;
        const coincideComision = this.filtroComision ? emp.porcentajeComision == this.filtroComision : true;
        
        return coincideNombre && coincideEstado && coincideComision;
      });
    },
    empleadosActivos() {
      return this.empleados.filter(e => e.estado === 'activo').length;
    },
    totalServiciosHoy() {
      // Nota: Esto requeriría que el backend envíe este dato calculado. 
      // Por ahora devolvemos 0 para no romper la vista.
      return this.empleados.reduce((total, e) => total + (e.serviciosHoy || 0), 0);
    },
    totalComisionesHoy() {
      return this.empleados.reduce((total, e) => total + (e.comisionHoy || 0), 0);
    }
  },
  methods: {
    async cargarEmpleados() {
      try {
        const response = await api.getEmpleados();
        const data = response.data || response;

        if(Array.isArray(data)) {
          this.empleados = data.map(e => ({
            id: e.id,
            nombre: e.nombre,
            rut: e.rut,
            telefono: e.telefono,
            email: e.email,
            // Mapeamos snake_case (Python) a camelCase (JS) si es necesario
            porcentajeComision: e.porcentaje_comision, 
            fechaIngreso: e.fecha_ingreso,
            estado: e.estado || 'activo',
            // Estos campos vendrán en 0 hasta que el backend los calcule
            serviciosHoy: 0, 
            comisionHoy: 0 
          }));
        }
      } catch (error) {
        console.error("Error cargando empleados:", error);
      }
    },

    async guardarEmpleado() {
      if (!this.form.nombre || !this.form.rut) {
        alert("Nombre y RUT son obligatorios");
        return;
      }

      try {
        // Enviamos el formulario tal cual lo espera Pydantic en el backend
        const payload = {
          nombre: this.form.nombre,
          rut: this.form.rut,
          telefono: this.form.telefono,
          email: this.form.email,
          porcentaje_comision: parseInt(this.form.porcentaje_comision)
        };

        await api.createEmpleado(payload);
        alert("Empleado registrado correctamente");
        
        this.cargarEmpleados();
        this.limpiarFormulario();
        
        // Cerrar modal
        document.getElementById('btnCerrarModalEmp').click();
        
      } catch (error) {
        console.error("Error al guardar:", error);
        alert("Error al guardar empleado. Verifica el RUT o la conexión.");
      }
    },

    limpiarFormulario() {
      this.form = {
        id: null,
        nombre: '',
        rut: '',
        telefono: '',
        email: '',
        porcentaje_comision: 40
      };
    }
  }
}
</script>