
// Centralized Axios client for every call the frontend makes to the backend.
// Goal: keep auth handling in one place so pages stay simple and beginners can see
// where tokens are attached and refreshed.
import axios, { InternalAxiosRequestConfig } from "axios";


// Base URL for API requests. Prefer env var so builds can point to prod/stage; fall back to local dev.
const API_BASE =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api";


// Create an Axios instance with the base URL so every request inherits it.
const api = axios.create({ baseURL: API_BASE });

// Single-flight refresh guard: if many calls 401 at once, only refresh one time.
let refreshInFlight: Promise<string> | null = null;


// Request interceptor: before any call goes out, attach the access token (except for login).
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("accessToken"); // match auth.ts storage key
    const url = config.url || "";
    const isLogin = url.endsWith("accounts/login/");
    if (token && !isLogin) {
      config.headers = config.headers || {};
      (config.headers as any)["Authorization"] = `Bearer ${token}`;
    }
    console.log('Request interceptor:', { tokenPresent: !!token, url, isLogin });
    return config;
  },
  (error) => Promise.reject(error)
);


// Response interceptor: if the server says 401 (expired), try one refresh, then retry the call.
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    console.log('Response interceptor: error status', error.response?.status, 'URL:', originalRequest?.url);

    // If access token is expired and we haven't retried yet (not for login URL)
    const originalUrl = originalRequest?.url || "";
    const isLogin = originalUrl.endsWith("accounts/login/");
    if (error.response?.status === 401 && !originalRequest._retry && !isLogin) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refreshToken");

      console.log('Attempting refresh, refreshToken present?', !!refreshToken);

      if (refreshToken) {
        // Ensure only one refresh request runs at a time
        if (!refreshInFlight) {
          const refreshTokenUsed = refreshToken; // snapshot to detect session changes
          refreshInFlight = axios
            .post(`${API_BASE}/token/refresh/`, { refresh: refreshTokenUsed })
            .then((res) => {
              const newAccessToken = res.data.access as string;
              localStorage.setItem("accessToken", newAccessToken);
              console.log('Refresh successful, new token set');
              return newAccessToken;
            })
            .catch((refreshError) => {
              console.log('Refresh failed:', axios.isAxiosError(refreshError) ? refreshError.response?.status : refreshError);
              // Only clear tokens if the current session still matches the token we attempted
              const currentRefresh = localStorage.getItem("refreshToken");
              if (currentRefresh === refreshTokenUsed) {
                localStorage.removeItem("accessToken");
                localStorage.removeItem("refreshToken");
                // Avoid redirect loops during login; only redirect if not already on login
                if (window.location.pathname !== "/login") {
                  window.location.href = "/login";
                }
              }
              throw refreshError;
            })
            .finally(() => {
              // Allow future refresh attempts
              refreshInFlight = null;
            });
        }

        try {
          const newAccessToken = await refreshInFlight;
          // Retry the original request with the new access token
          originalRequest.headers = originalRequest.headers || {};
          (originalRequest.headers as any)["Authorization"] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        } catch {
          // Already handled above (tokens cleared + redirect); propagate error
          return Promise.reject(error);
        }
      }
    }

    return Promise.reject(error);
  }
);


// Export the configured Axios instance for use in all API calls
export default api;