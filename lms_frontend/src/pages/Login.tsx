
// This component provides a login form for users to sign in to the LMS.
// It handles user input, calls the login API, and manages error feedback.
import React, { useState } from "react";
import { loginUser } from "../services/auth";


const Login: React.FC = () => {
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
      // loginUser stores tokens in localStorage if successful
      const data = await loginUser({ username, password });
      console.log("Logged in successfully:", data);
      // Redirect to profile page after successful login
      window.location.href = "/profile";
    } catch (err: any) {
      // Show error message if login fails
      setError(err.message || "Login failed");
    }
  };

  // Render the login form UI
  return (
    <div className="login-container auth-container">
      <h2 className="auth-title">Login</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="auth-field">
          <label className="auth-label">Username</label>
          <input
            className="auth-input"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="auth-field">
          <label className="auth-label">Password</label>
          <input
            className="auth-input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button className="auth-button" type="submit">Login</button>
      </form>

      {error && <p className="auth-error">{error}</p>}
    </div>
  );
};


// Export the Login component so it can be used in routing and other pages.
export default Login;