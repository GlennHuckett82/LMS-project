
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
      // Redirect to homepage after successful login
      window.location.href = "/";
    } catch (err: any) {
      // Show error message if login fails
      setError(err.message || "Login failed");
    }
  };

  // Render the login form UI
  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          {/* Controlled input for username */}
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Password</label>
          {/* Controlled input for password */}
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Login</button>
      </form>

      {/* Show error message if login fails */}
      {error && <p className="error">{error}</p>}
    </div>
  );
};


// Export the Login component so it can be used in routing and other pages.
export default Login;