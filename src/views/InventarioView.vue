<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-box-seam me-2"></i>
          Gestión de Inventario
        </h2>
        <p class="text-muted">Administra los insumos y stock del lavadero</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-success me-2" data-bs-toggle="modal" data-bs-target="#modalMovimiento">
          <i class="bi bi-arrow-down-circle me-2"></i>
          Registrar Entrada
        </button>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalInsumo">
          <i class="bi bi-plus-circle me-2"></i>
          Nuevo Insumo
        </button>
      </div>
    </div>

    <!-- Alertas de stock bajo -->
    <div v-if="insumosStockBajo.length > 0" class="alert alert-warning mb-4">
      <h5 class="alert-heading">
        <i class="bi bi-exclamation-triangle me-2"></i>
        Alertas de Stock Bajo
      </h5>
      <p class="mb-0">
        Hay {{ insumosStockBajo.length }} insumo(s) con stock bajo. Revisa la tabla para más detalles.
      </p>
    </div>

    <!-- Resumen de inventario -->
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-primary">
          <div class="card-body">
            <h6 class="text-muted mb-1">Total Insumos</h6>
            <h3 class="mb-0">{{ insumos.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-success">
          <div class="card-body">
            <h6 class="text-muted mb-1">Stock Óptimo</h6>
            <h3 class="mb-0 text-success">{{ insumosStockOptimo }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-warning">
          <div class="card-body">
            <h6 class="text-muted mb-1">Stock Bajo</h6>
            <h3 class="mb-0 text-warning">{{ insumosStockBajo.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-info">
          <div class="card-body">
            <h6 class="text-muted mb-1">Valor Total</h6>
            <h3 class="mb-0 text-info">${{ valorTotalInventario.toLocaleString() }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Buscar insumo..."
              v-model="busqueda"
            >
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroCategoria">
              <option value="">Todas las categorías</option>
              <option value="quimicos">Químicos</option>
              <option value="ceras">Ceras</option>
              <option value="herramientas">Herramientas</option>
              <option value="accesorios">Accesorios</option>
              <option value="otros">Otros</option>
            </select>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroEstado">
              <option value="">Todos los estados</option>
              <option value="optimo">Stock Óptimo</option>
              <option value="bajo">Stock Bajo</option>
              <option value="critico">Stock Crítico</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla de inventario -->
    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Categoría</th>
                <th>Stock Actual</th>
                <th>Stock Mínimo</th>
                <th>Unidad</th>
                <th>Precio Unitario</th>
                <th>Valor Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="insumo in insumos" :key="insumo.id">
                <td>#{{ insumo.id }}</td>
                <td>
                  <strong>{{ insumo.nombre }}</strong>
                </td>
                <td>
                  <span class="badge bg-secondary">{{ insumo.categoria }}</span>
                </td>
                <td>
                  <strong :class="insumo.stock <= insumo.stockMinimo ? 'text-danger' : 'text-success'">
                    {{ insumo.stock }}
                  </strong>
                </td>
                <td>{{ insumo.stockMinimo }}</td>
                <td>{{ insumo.unidad }}</td>
                <td>${{ insumo.precioUnitario.toLocaleString() }}</td>
                <td class="fw-bold">${{ (insumo.stock * insumo.precioUnitario).toLocaleString() }}</td>
                <td>
                  <span :class="'badge bg-' + insumo.estadoColor">
                    {{ insumo.estadoTexto }}
                  </span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button 
                      class="btn btn-outline-success" 
                      title="Agregar stock"
                      data-bs-toggle="modal" 
                      data-bs-target="#modalMovimiento"
                      @click="seleccionarInsumo(insumo)"
                    >
                      <i class="bi bi-plus-circle"></i>
                    </button>
                    <button 
                      class="btn btn-outline-warning" 
                      title="Editar"
                      data-bs-toggle="modal" 
                      data-bs-target="#modalInsumo"
                      @click="editarInsumo(insumo)"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-primary" title="Historial">
                      <i class="bi bi-clock-history"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal para nuevo insumo -->
    <div class="modal fade" id="modalInsumo" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-box-seam me-2"></i>
              {{ modoEdicion ? 'Editar Insumo' : 'Nuevo Insumo' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">Nombre del Insumo *</label>
                <input type="text" class="form-control" v-model="insumoForm.nombre" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Categoría *</label>
                <select class="form-select" v-model="insumoForm.categoria" required>
                  <option value="">Seleccionar...</option>
                  <option value="quimicos">Químicos</option>
                  <option value="ceras">Ceras</option>
                  <option value="herramientas">Herramientas</option>
                  <option value="accesorios">Accesorios</option>
                  <option value="otros">Otros</option>
                </select>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Stock {{ modoEdicion ? 'Actual' : 'Inicial' }} *</label>
                  <input type="number" class="form-control" v-model="insumoForm.stock" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Stock Mínimo *</label>
                  <input type="number" class="form-control" v-model="insumoForm.stockMinimo" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Unidad de Medida *</label>
                  <select class="form-select" v-model="insumoForm.unidad" required>
                    <option value="">Seleccionar...</option>
                    <option value="litro">Litro</option>
                    <option value="kilo">Kilogramo</option>
                    <option value="unidad">Unidad</option>
                    <option value="caja">Caja</option>
                    <option value="galon">Galón</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Precio Unitario *</label>
                  <input type="number" class="form-control" v-model="insumoForm.precioUnitario" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <textarea class="form-control" rows="2" v-model="insumoForm.descripcion"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary" @click="guardarInsumo">
              <i class="bi bi-save me-2"></i>
              {{ modoEdicion ? 'Actualizar' : 'Guardar' }} Insumo
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para movimiento de inventario -->
    <div class="modal fade" id="modalMovimiento" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-arrow-down-circle me-2"></i>
              Registrar Entrada de Stock
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">Insumo *</label>
                <select class="form-select" v-model="movimientoForm.insumoId" required>
                  <option value="">Seleccionar insumo...</option>
                  <option v-for="insumo in insumos" :key="insumo.id" :value="insumo.id">
                    {{ insumo.nombre }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Cantidad *</label>
                <input type="number" class="form-control" v-model="movimientoForm.cantidad" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Motivo *</label>
                <select class="form-select" v-model="movimientoForm.motivo" required>
                  <option value="">Seleccionar...</option>
                  <option value="compra">Compra</option>
                  <option value="devolucion">Devolución</option>
                  <option value="ajuste">Ajuste de inventario</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Observaciones</label>
                <textarea class="form-control" rows="2" v-model="movimientoForm.observaciones"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-success" @click="registrarMovimiento">
              <i class="bi bi-check-circle me-2"></i>
              Registrar Entrada
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as bootstrap from 'bootstrap'
import api from '@/services/api'

export default {
  name: 'InventarioView',
  data() {
    return {
      busqueda: '',
      filtroCategoria: '',
      filtroEstado: '',
      modoEdicion: false,
      insumos: [],
      insumoForm: {
        id: null,
        nombre: '',
        categoria: '',
        stock: 0,
        stockMinimo: 0,
        unidad: '',
        precioUnitario: 0,
        descripcion: ''
      },
      movimientoForm: {
        insumoId: '',
        cantidad: 0,
        motivo: '',
        observaciones: ''
      }
    }
  },
  mounted() {
    this.cargarInventario()
  },
  computed: {
    insumosStockBajo() {
      return this.insumos.filter(i => i.stock <= i.stockMinimo)
    },
    insumosStockOptimo() {
      return this.insumos.filter(i => i.stock > i.stockMinimo).length
    },
    valorTotalInventario() {
      return this.insumos.reduce((total, insumo) => {
        return total + (insumo.stock * insumo.precioUnitario)
      }, 0)
    }
  },
  methods: {
    async cargarInventario() {
      try {
        const response = await api.getInventario()
        const data = Array.isArray(response) ? response : response?.data || []

        // Mapear los datos de snake_case (API) a camelCase (frontend)
        this.insumos = data.map(insumo => ({
          id: insumo.id,
          nombre: insumo.nombre,
          categoria: insumo.categoria,
          stock: insumo.stock,
          stockMinimo: insumo.stock_minimo,
          unidad: insumo.unidad,
          precioUnitario: insumo.precio_unitario,
          descripcion: insumo.descripcion,
          estadoTexto: this.mapearEstadoTexto(insumo.estado_stock),
          estadoColor: this.mapearEstadoColor(insumo.estado_stock)
        }))
      } catch (error) {
        console.error('Error al cargar inventario:', error)
      }
    },
    mapearEstadoTexto(estadoStock) {
      const mapeo = {
        'optimo': 'Stock Óptimo',
        'bajo': 'Stock Bajo',
        'critico': 'Stock Crítico'
      }
      return mapeo[estadoStock] || 'Desconocido'
    },
    mapearEstadoColor(estadoStock) {
      const mapeo = {
        'optimo': 'success',
        'bajo': 'warning',
        'critico': 'danger'
      }
      return mapeo[estadoStock] || 'secondary'
    },
    seleccionarInsumo(insumo) {
      this.movimientoForm.insumoId = insumo.id
    },
    editarInsumo(insumo) {
      this.modoEdicion = true
      this.insumoForm = {
        id: insumo.id,
        nombre: insumo.nombre,
        categoria: insumo.categoria,
        stock: insumo.stock,
        stockMinimo: insumo.stockMinimo,
        unidad: insumo.unidad,
        precioUnitario: insumo.precioUnitario,
        descripcion: insumo.descripcion || ''
      }
    },
    async guardarInsumo() {
      try {
        // Mapear los datos de camelCase (frontend) a snake_case (API)
        const insumoData = {
          nombre: this.insumoForm.nombre,
          categoria: this.insumoForm.categoria,
          stock: parseFloat(this.insumoForm.stock),
          stock_minimo: parseFloat(this.insumoForm.stockMinimo),
          unidad: this.insumoForm.unidad,
          precio_unitario: parseFloat(this.insumoForm.precioUnitario),
          descripcion: this.insumoForm.descripcion
        }

        if (this.modoEdicion) {
          // TODO: Implementar api.updateInsumo cuando esté disponible
          console.log('Actualizar insumo:', insumoData)
          alert('Función de actualización pendiente de implementar')
        } else {
          await api.createInsumo(insumoData)
          alert('Insumo creado correctamente')
          // Recargar el inventario después de crear
          await this.cargarInventario()
        }

        this.limpiarFormInsumo()
        // Cerrar el modal
        const modal = document.getElementById('modalInsumo')
        const bsModal = bootstrap.Modal.getInstance(modal)
        if (bsModal) bsModal.hide()
      } catch (error) {
        console.error('Error al guardar insumo:', error)
        alert('Error al guardar el insumo. Por favor, intenta nuevamente.')
      }
    },
    async registrarMovimiento() {
      try {
        // Mapear los datos para el movimiento de entrada
        const movimientoData = {
          id_insumo: parseInt(this.movimientoForm.insumoId),
          tipo_movimiento: 'entrada',
          cantidad: parseFloat(this.movimientoForm.cantidad),
          motivo: this.movimientoForm.motivo,
          usuario: 'admin'
        }

        await api.registrarMovimiento(movimientoData)
        alert('Movimiento registrado correctamente')

        // Recargar el inventario después de registrar la entrada
        await this.cargarInventario()

        this.limpiarFormMovimiento()
        // Cerrar el modal
        const modal = document.getElementById('modalMovimiento')
        const bsModal = bootstrap.Modal.getInstance(modal)
        if (bsModal) bsModal.hide()
      } catch (error) {
        console.error('Error al registrar movimiento:', error)
        alert('Error al registrar el movimiento. Por favor, intenta nuevamente.')
      }
    },
    limpiarFormInsumo() {
      this.modoEdicion = false
      this.insumoForm = {
        id: null,
        nombre: '',
        categoria: '',
        stock: 0,
        stockMinimo: 0,
        unidad: '',
        precioUnitario: 0,
        descripcion: ''
      }
    },
    limpiarFormMovimiento() {
      this.movimientoForm = {
        insumoId: '',
        cantidad: 0,
        motivo: '',
        observaciones: ''
      }
    }
  }
}
</script>
