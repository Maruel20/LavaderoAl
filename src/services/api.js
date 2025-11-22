import axios from 'axios';

// Asegúrate de que este puerto coincida con tu uvicorn (8000 o 5000)
const API_URL = 'http://localhost:8000/api';

export default {
    // --- AUTH ---
    async login(username, password) {
        const response = await axios.post(`${API_URL}/login`, { username, password });
        return response.data;
    },

    // --- SERVICIOS ---
    async getServicios() {
        const response = await axios.get(`${API_URL}/servicios`);
        return response.data;
    },
    async createServicio(servicio) {
        const response = await axios.post(`${API_URL}/servicios`, servicio);
        return response.data;
    },

    // --- EMPLEADOS ---
    async getEmpleados() {
        const response = await axios.get(`${API_URL}/empleados`);
        return response.data;
    },
    async createEmpleado(empleado) {
        const response = await axios.post(`${API_URL}/empleados`, empleado);
        return response.data;
    },

    // --- INVENTARIO ---
    async getInventario() {
        const response = await axios.get(`${API_URL}/inventario`);
        return response.data;
    },
    async createInsumo(insumo) {
        const response = await axios.post(`${API_URL}/inventario`, insumo);
        return response.data;
    },
    async updateInsumo(id, insumo) {
        const response = await axios.put(`${API_URL}/inventario/${id}`, insumo);
        return response.data;
    },
    async registrarMovimiento(movimiento) {
        const response = await axios.post(`${API_URL}/inventario/movimiento`, movimiento);
        return response.data;
    },
    async getMovimientosInsumo(id) {
        const response = await axios.get(`${API_URL}/inventario/movimientos/${id}`);
        return response.data;
    },
    async getAlertasInventario() {
        const response = await axios.get(`${API_URL}/inventario/alertas`);
        return response.data;
    },

    // --- LIQUIDACIONES ---
    async getLiquidaciones() {
        const response = await axios.get(`${API_URL}/liquidaciones`);
        return response.data;
    },
    async getLiquidacionDetalle(id) {
        const response = await axios.get(`${API_URL}/liquidaciones/${id}`);
        return response.data;
    },
    async calcularLiquidacion(liquidacion) {
        const response = await axios.post(`${API_URL}/liquidaciones/calcular`, liquidacion);
        return response.data;
    },
    async marcarLiquidacionPagada(id) {
        const response = await axios.put(`${API_URL}/liquidaciones/${id}/pagar`);
        return response.data;
    },
    async getLiquidacionesEmpleado(idEmpleado) {
        const response = await axios.get(`${API_URL}/liquidaciones/empleado/${idEmpleado}`);
        return response.data;
    },

    // --- CONVENIOS ---
    async getConvenios() {
        const response = await axios.get(`${API_URL}/convenios`);
        return response.data;
    },
    async getConvenioDetalle(id) {
        const response = await axios.get(`${API_URL}/convenios/${id}`);
        return response.data;
    },
    async createConvenio(convenio) {
        const response = await axios.post(`${API_URL}/convenios`, convenio);
        return response.data;
    },
    async updateConvenio(id, convenio) {
        const response = await axios.put(`${API_URL}/convenios/${id}`, convenio);
        return response.data;
    },
    async addVehiculoConvenio(idConvenio, vehiculo) {
        const response = await axios.post(`${API_URL}/convenios/${idConvenio}/vehiculos`, vehiculo);
        return response.data;
    },
    async getVehiculosConvenio(idConvenio) {
        const response = await axios.get(`${API_URL}/convenios/${idConvenio}/vehiculos`);
        return response.data;
    },
    async removeVehiculoConvenio(idVehiculo) {
        const response = await axios.delete(`${API_URL}/convenios/vehiculos/${idVehiculo}`);
        return response.data;
    },
    async verificarConvenioPatente(patente) {
        const response = await axios.get(`${API_URL}/convenios/patente/${patente}`);
        return response.data;
    },

    // --- TARIFAS ---
    async getTarifas() {
        const response = await axios.get(`${API_URL}/tarifas`);
        return response.data;
    },
    async getTarifaEspecifica(tipoVehiculo, tipoServicio) {
        const response = await axios.get(`${API_URL}/tarifas/${tipoVehiculo}/${tipoServicio}`);
        return response.data;
    },
    async updateTarifa(tipoVehiculo, tipoServicio, precio) {
        const response = await axios.put(`${API_URL}/tarifas/${tipoVehiculo}/${tipoServicio}`, { precio });
        return response.data;
    },
    async getTarifasVehiculo(tipoVehiculo) {
        const response = await axios.get(`${API_URL}/tarifas/vehiculo/${tipoVehiculo}`);
        return response.data;
    },
    async getTiposVehiculos() {
        const response = await axios.get(`${API_URL}/tarifas/tipos/vehiculos`);
        return response.data;
    },
    async getTiposServicios() {
        const response = await axios.get(`${API_URL}/tarifas/tipos/servicios`);
        return response.data;
    },

    // --- REPORTES ---
    async getReporteGeneral(fechaInicio, fechaFin) {
        const params = {};
        if (fechaInicio) params.fecha_inicio = fechaInicio;
        if (fechaFin) params.fecha_fin = fechaFin;
        const response = await axios.get(`${API_URL}/reportes/general`, { params });
        return response.data;
    },
    async getReporteEmpleados(fechaInicio, fechaFin) {
        const params = {};
        if (fechaInicio) params.fecha_inicio = fechaInicio;
        if (fechaFin) params.fecha_fin = fechaFin;
        const response = await axios.get(`${API_URL}/reportes/empleados`, { params });
        return response.data;
    },
    async getReporteServiciosDiarios(dias = 30) {
        const response = await axios.get(`${API_URL}/reportes/servicios-diarios`, { params: { dias } });
        return response.data;
    },
    async getReporteConvenios(fechaInicio, fechaFin) {
        const params = {};
        if (fechaInicio) params.fecha_inicio = fechaInicio;
        if (fechaFin) params.fecha_fin = fechaFin;
        const response = await axios.get(`${API_URL}/reportes/convenios`, { params });
        return response.data;
    },
    async getReporteInventario() {
        const response = await axios.get(`${API_URL}/reportes/inventario`);
        return response.data;
    },
    async getReporteFinanciero(anio) {
        const params = {};
        if (anio) params.anio = anio;
        const response = await axios.get(`${API_URL}/reportes/financiero`, { params });
        return response.data;
    },

    // --- DASHBOARD ---
    async getMetricasDashboard() {
        const response = await axios.get(`${API_URL}/dashboard/metricas`);
        return response.data;
    },
    async getServiciosRecientes(limit = 10) {
        const response = await axios.get(`${API_URL}/dashboard/servicios-recientes`, { params: { limit } });
        return response.data;
    },
    async getAlertasInventarioDashboard() {
        const response = await axios.get(`${API_URL}/dashboard/alertas-inventario`);
        return response.data;
    },
    async getEmpleadosTop(limit = 5) {
        const response = await axios.get(`${API_URL}/dashboard/empleados-top`, { params: { limit } });
        return response.data;
    },
    async getGraficoServicios(dias = 7) {
        const response = await axios.get(`${API_URL}/dashboard/grafico-servicios`, { params: { dias } });
        return response.data;
    },
    async getServiciosPorTipo() {
        const response = await axios.get(`${API_URL}/dashboard/servicios-por-tipo`);
        return response.data;
    },
    async getLiquidacionesPendientes() {
        const response = await axios.get(`${API_URL}/dashboard/liquidaciones-pendientes`);
        return response.data;
    }
};