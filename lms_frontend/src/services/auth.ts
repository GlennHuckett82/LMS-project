import api from "./api";

/**
 * Data shape for user registration.
 * Registration requires username, email, and password.
 */
interface RegisterData {
  username: string;
  email: string;
  password: string;
}

/**
 * Register a new user.
 * Sends POST to /api/accounts/register/ with username, email, password.
 * Expected response: { id, username, email }
 */
export async function registerUser(data: RegisterData) {
  const response = await api.post("/accounts/register/", data);
  return response.data;
}

/**
 * Data shape for user login.
 * Login requires username + password.
 */
interface LoginData {
  username: string;
  password: string;
}

/**
 * Log in an existing user.
 * Sends POST to /api/accounts/login/ with username, password.
 * Expected response from SimpleJWT:
 * {
 *   "refresh": "<refresh_token>",
 *   "access": "<access_token>"
 * }
 */
export async function loginUser(data: LoginData) {
  const response = await api.post("/accounts/login/", data);

  // Store tokens for later use
  localStorage.setItem("accessToken", response.data.access);
  localStorage.setItem("refreshToken", response.data.refresh);

  return response.data;
}