import axios from 'axios';

// Asegúrate de que este puerto coincida con tu uvicorn (8000 o 5000)
const API_URL = 'http://localhost:8000/api';

export default {
    async login(username, password) {
        const response = await axios.post(`${API_URL}/login`, { username, password });
        return response.data;
    },
    async getServicios() {
        const response = await axios.get(`${API_URL}/servicios`);
        return response.data;
    },
    async createServicio(servicio) {
        const response = await axios.post(`${API_URL}/servicios`, servicio);
        return response.data;
    },
    async getEmpleados() {
        const response = await axios.get(`${API_URL}/empleados`);
        return response.data;
    },
    // --- ESTA ES LA FUNCIÓN QUE TE FALTABA ---
    async createEmpleado(empleado) {
        const response = await axios.post(`${API_URL}/empleados`, empleado);
        return response.data;
    }
    
};