// This component provides a login form for users to sign in to the LMS.
// It handles user input, calls the login API, and manages error feedback.
import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { loginUser, fetchMe } from "../services/auth";
import PasswordField from "../components/PasswordField";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import { useAuth } from "../auth/AuthContext";
 

interface DecodedToken {
  user_id: number;
  role: 'student' | 'teacher' | 'admin';
  exp: number;
  iat: number;
}

// Using text labels instead of icons to avoid TypeScript issues

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  // State for the username input field
  const [username, setUsername] = useState("");
  // State for the password input field
  const [password, setPassword] = useState("");
  // State for any error messages (null means no error)
  const [error, setError] = useState<string | null>(null);

  // Handles form submission for login
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page reload
    setError(null); // Clear any previous error

    try {
      // Call the login API with username and password
      const data = await loginUser({ username, password });
      console.log("Logged in successfully:", data);

      // Update global auth state and persist tokens
      login(data.access, data.refresh);

      // Prefer server-authoritative role via /accounts/me/ to avoid claim mismatches
      let userRole: string | null = null;
      try {
        const me = await fetchMe();
        console.log('fetchMe result:', me);
        // Treat staff/superuser as admin if role is missing or student
        const roleFromApi = (me.role ?? "").toLowerCase();
        if (roleFromApi === 'admin' || me.is_superuser || me.is_staff) {
          userRole = 'admin';
        } else {
          userRole = roleFromApi;
        }
      } catch (e) {
        // Fallback to decoding the token if /me fails
        const decodedToken = jwtDecode<DecodedToken & Record<string, any>>(data.access);
        console.log('decoded token:', decodedToken);
        const rawRole = (decodedToken as any)?.role ?? (decodedToken as any)?.user_role ?? (decodedToken as any)?.roleName ?? "";
        userRole = String(rawRole).toLowerCase();
      }
      console.log('Resolved userRole:', userRole);

      // Navigate to the correct dashboard based on the user's role
      switch (userRole) {
        case 'teacher':
          navigate("/teacher-dashboard");
          break;
        case 'admin':
          navigate("/admin-dashboard");
          break;
        default:
          navigate("/profile");
          break;
      }
    } catch (err: any) {
      // Show error message if login fails
      console.error("Login error:", err); // Log the full error to the console
      if (axios.isAxiosError(err) && err.response) {
        // If it's an API error, show the message from the backend
        setError(err.response.data.detail || "Login failed. Please check your credentials.");
      } else {
        // For other errors (network, etc.)
        setError(err.message || "An unexpected error occurred.");
      }
    }
  };

  // Render the login form UI
  return (
    <div className="login-container auth-container">
      <h2 className="auth-title">Login</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="auth-field">
          <label className="auth-label" htmlFor="username">Username</label>
          <input
            className="auth-input"
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </div>
        <PasswordField
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
        <button className="auth-button" type="submit">Login</button>
      </form>
      {error && <div className="auth-error">{error}</div>}
    </div>
  );
};

// Export the Login component so it can be used in routing and other pages.
export default Login;