import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";

interface RequireAuthProps {
  children: React.ReactNode;
}

// HOC to protect routes and redirect unauthenticated users
const RequireAuth: React.FC<RequireAuthProps> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to login, preserve attempted route for redirect after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  // Always return a valid React element or null
  return <>{children}</>;
};

export default RequireAuth;
