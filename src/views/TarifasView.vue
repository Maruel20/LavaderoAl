<template>
  <div class="container-fluid py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="mb-1">Configuración de Tarifas</h2>
        <p class="text-muted">Define los precios según tipo de vehículo y servicio</p>
      </div>
    </div>

     Tabla de Tarifas 
    <div class="card shadow-sm">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Tipo de Vehículo</th>
                <th>Enjuague</th>
                <th>Lavado Básico</th>
                <th>Lavado Completo</th>
                <th>Lavado + Brillado</th>
                <th>Lavado Premium</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tarifa in tarifas" :key="tarifa.id">
                <td><strong>{{ tarifa.tipoVehiculo }}</strong></td>
                <td>
                  <input 
                    type="number" 
                    class="form-control form-control-sm" 
                    v-model="tarifa.enjuague"
                    @change="guardarCambios(tarifa)"
                  >
                </td>
                <td>
                  <input 
                    type="number" 
                    class="form-control form-control-sm" 
                    v-model="tarifa.lavadoBasico"
                    @change="guardarCambios(tarifa)"
                  >
                </td>
                <td>
                  <input 
                    type="number" 
                    class="form-control form-control-sm" 
                    v-model="tarifa.lavadoCompleto"
                    @change="guardarCambios(tarifa)"
                  >
                </td>
                <td>
                  <input 
                    type="number" 
                    class="form-control form-control-sm" 
                    v-model="tarifa.lavadoBrillado"
                    @change="guardarCambios(tarifa)"
                  >
                </td>
                <td>
                  <input 
                    type="number" 
                    class="form-control form-control-sm" 
                    v-model="tarifa.lavadoPremium"
                    @change="guardarCambios(tarifa)"
                  >
                </td>
                <td>
                  <button class="btn btn-sm btn-success" @click="guardarCambios(tarifa)">
                    <i class="bi bi-check-lg"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="alert alert-info mt-3">
          <i class="bi bi-info-circle me-2"></i>
          <strong>Nota:</strong> Los precios se autocompletarán al registrar servicios, pero podrás editarlos manualmente si es necesario.
        </div>
      </div>
    </div>

     Tipos de Servicio 
    <div class="card shadow-sm mt-4">
      <div class="card-header bg-white">
        <h5 class="mb-0">Tipos de Servicio Disponibles</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-4" v-for="servicio in tiposServicio" :key="servicio.id">
            <div class="card mb-3 border-primary">
              <div class="card-body">
                <h6 class="card-title">{{ servicio.nombre }}</h6>
                <p class="card-text text-muted small">{{ servicio.descripcion }}</p>
                <span class="badge bg-primary">{{ servicio.duracion }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'TarifasView',
  data() {
    return {
      tarifas: [
        {
          id: 1,
          tipoVehiculo: 'Moto',
          enjuague: 3000,
          lavadoBasico: 5000,
          lavadoCompleto: 7000,
          lavadoBrillado: 9000,
          lavadoPremium: 12000
        },
        {
          id: 2,
          tipoVehiculo: 'Auto Pequeño',
          enjuague: 5000,
          lavadoBasico: 8000,
          lavadoCompleto: 12000,
          lavadoBrillado: 15000,
          lavadoPremium: 20000
        },
        {
          id: 3,
          tipoVehiculo: 'Auto Grande',
          enjuague: 6000,
          lavadoBasico: 10000,
          lavadoCompleto: 15000,
          lavadoBrillado: 18000,
          lavadoPremium: 25000
        },
        {
          id: 4,
          tipoVehiculo: 'Camioneta/SUV',
          enjuague: 8000,
          lavadoBasico: 12000,
          lavadoCompleto: 18000,
          lavadoBrillado: 22000,
          lavadoPremium: 30000
        },
        {
          id: 5,
          tipoVehiculo: 'Camión',
          enjuague: 10000,
          lavadoBasico: 15000,
          lavadoCompleto: 22000,
          lavadoBrillado: 28000,
          lavadoPremium: 35000
        }
      ],
      tiposServicio: []
    }
  },
  mounted() {
    this.cargarTiposServicio()
  },
  methods: {
    async cargarTiposServicio() {
      try {
        const data = await api.getTiposServicios()
        this.tiposServicio = data.map(s => ({
          id: s.tipo_servicio,
          nombre: this.formatearNombreServicio(s.tipo_servicio),
          descripcion: s.descripcion || '',
          duracion: this.estimarDuracion(s.tipo_servicio)
        }))
      } catch (error) {
        console.error('Error al cargar tipos de servicio:', error)
        this.tiposServicio = [
          {
            id: 1,
            nombre: 'Lavado Simple',
            descripcion: 'Lavado exterior básico',
            duracion: '15-20 min'
          },
          {
            id: 2,
            nombre: 'Lavado Completo',
            descripcion: 'Exterior, interior, aspirado y limpieza de vidrios',
            duracion: '40-50 min'
          },
          {
            id: 3,
            nombre: 'Encerado',
            descripcion: 'Aplicación de cera y brillo',
            duracion: '30-40 min'
          },
          {
            id: 4,
            nombre: 'Lavado Motor',
            descripcion: 'Limpieza del compartimento del motor',
            duracion: '20-30 min'
          },
          {
            id: 5,
            nombre: 'Pulido',
            descripcion: 'Pulido profesional de la pintura',
            duracion: '90-120 min'
          },
          {
            id: 6,
            nombre: 'Descontaminación',
            descripcion: 'Descontaminación de pintura',
            duracion: '60-90 min'
          }
        ]
      }
    },
    formatearNombreServicio(tipo) {
      const nombres = {
        'lavado_simple': 'Lavado Simple',
        'lavado_completo': 'Lavado Completo',
        'encerado': 'Encerado',
        'lavado_motor': 'Lavado Motor',
        'pulido': 'Pulido',
        'descontaminacion': 'Descontaminación'
      }
      return nombres[tipo] || tipo
    },
    estimarDuracion(tipo) {
      const duraciones = {
        'lavado_simple': '15-20 min',
        'lavado_completo': '40-50 min',
        'encerado': '30-40 min',
        'lavado_motor': '20-30 min',
        'pulido': '90-120 min',
        'descontaminacion': '60-90 min'
      }
      return duraciones[tipo] || '30 min'
    },
    guardarCambios(tarifa) {
      alert('Tarifa actualizada correctamente (vista actual usa tarifas hardcoded)')
      console.log('Guardando cambios de tarifa:', tarifa)
    }
  }
}
</script>

<style scoped>
.form-control-sm {
  max-width: 120px;
}

.table td input {
  text-align: right;
}
</style>
