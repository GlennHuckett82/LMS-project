
// Centralized Axios instance for all API requests in the LMS frontend.
// Handles authentication tokens and automatic refresh on expiration.
import axios, { InternalAxiosRequestConfig, AxiosError } from "axios";


// Base URL for API requests. Uses environment variable if set, otherwise defaults to local backend.
const API_BASE =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api";


// Create an Axios instance with the base URL
const api = axios.create({ baseURL: API_BASE });


// Request interceptor: attaches access token to every outgoing request if available
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("accessToken"); // match auth.ts storage key
    if (token && config.url !== '/accounts/login/') {
      config.headers = config.headers || {};
      (config.headers as any)["Authorization"] = `Bearer ${token}`;
    }
    console.log('Request interceptor: token present?', !!token, 'URL:', config.url);
    return config;
  },
  (error) => Promise.reject(error)
);


// Response interceptor: automatically refreshes access token if expired (401)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    console.log('Response interceptor: error status', error.response?.status, 'URL:', originalRequest?.url);

    // If access token is expired and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== '/accounts/login/') {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refreshToken");

      console.log('Attempting refresh, refreshToken present?', !!refreshToken);

      if (refreshToken) {
        try {
          // Attempt to refresh the access token using the refresh token
          const refreshResponse = await axios.post(
            `${API_BASE}/accounts/login/refresh/`,
            { refresh: refreshToken }
          );

          const newAccessToken = refreshResponse.data.access;
          localStorage.setItem("accessToken", newAccessToken);

          console.log('Refresh successful, new token set');

          // Retry the original request with the new access token
          originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        } catch (refreshError) {
          console.log('Refresh failed:', axios.isAxiosError(refreshError) ? refreshError.response?.status : refreshError);
          // If refresh fails, clear tokens and redirect to login page
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);


// Export the configured Axios instance for use in all API calls
export default api;