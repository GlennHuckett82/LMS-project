import axios, { InternalAxiosRequestConfig } from 'axios';

const API_BASE =
  process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // Axios v1+ uses AxiosHeaders internally, but mutation works fine
      config.headers = config.headers || {};
      (config.headers as any)['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;