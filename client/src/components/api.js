// api.js
import axios from 'axios';

// Create an instance of axios with a base URL
const api = axios.create({
  baseURL: 'http://localhost:5000',
});

// Add a request interceptor to include authentication token if available
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token'); // Retrieve the token from local storage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default api;
