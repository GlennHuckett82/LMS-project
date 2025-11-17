import axios, { InternalAxiosRequestConfig } from "axios";

const API_BASE =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api";

const api = axios.create({ baseURL: API_BASE });

// Request interceptor: attach access token if present
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("accessToken"); // match auth.ts storage key
    if (token) {
      config.headers = config.headers || {};
      (config.headers as any)["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle expired tokens by refreshing
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refreshToken");

      if (refreshToken) {
        try {
          const refreshResponse = await axios.post(
            `${API_BASE}/accounts/login/refresh/`,
            { refresh: refreshToken }
          );

          const newAccessToken = refreshResponse.data.access;
          localStorage.setItem("accessToken", newAccessToken);

          // Retry original request with new token
          originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed → clear tokens and redirect to login
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;