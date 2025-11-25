
// This component provides a registration form for new users to sign up for the LMS.
// It manages user input, calls the registration API, and displays feedback messages.
import React, { useState } from "react";
import { registerUser } from "../services/auth";


const Register: React.FC = () => {
  // State for the username input field
  const [username, setUsername] = useState("");
  // State for the email input field
  const [email, setEmail] = useState("");
  // State for the password input field
  const [password, setPassword] = useState("");
  // State for any error messages (null means no error)
  const [error, setError] = useState<string | null>(null);
  // State for success messages after registration
  const [success, setSuccess] = useState<string | null>(null);


  // Handles form submission for registration
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page reload
    setError(null); // Clear any previous error
    setSuccess(null); // Clear any previous success message

    try {
      // Call the registration API with username, email, and password
      // registerUser returns user data if successful
      const data = await registerUser({ username, email, password });
      setSuccess(`User ${data.username} registered successfully!`);
      // Clear input fields after successful registration
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (err: any) {
      // Show error message if registration fails
      setError(err.message || "Registration failed");
    }
  };


  // Render the registration form UI
  return (
    <div className="register-container auth-container">
      <h2 className="auth-title">Register</h2>
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
          <label className="auth-label">Email</label>
          <input
            className="auth-input"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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

        <button className="auth-button" type="submit">Register</button>
      </form>

      {error && <p className="auth-error">{error}</p>}
      {success && <p className="auth-success">{success}</p>}
    </div>
  );
};


// Export the Register component so it can be used in routing and other pages.
export default Register;