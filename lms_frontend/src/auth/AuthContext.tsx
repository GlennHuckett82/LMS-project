import React, { createContext, useContext, useEffect, useState, ReactNode } from "react";

interface AuthContextType {
  isAuthenticated: boolean;
  accessToken: string | null;
  // Login with new tokens; refresh is optional for flexibility
  login: (accessToken: string, refreshToken?: string) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(
    localStorage.getItem("accessToken")
  );
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!accessToken);

  useEffect(() => {
    setIsAuthenticated(!!accessToken);
  }, [accessToken]);

  // Listen for token expiration or removal
  useEffect(() => {
    const handleStorage = () => {
      const token = localStorage.getItem("accessToken");
      setAccessToken(token);
      setIsAuthenticated(!!token);
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, []);

  const login = (accessTokenValue: string, refreshTokenValue?: string) => {
    // Persist tokens for interceptors
    localStorage.setItem("accessToken", accessTokenValue);
    if (refreshTokenValue) {
      localStorage.setItem("refreshToken", refreshTokenValue);
    }
    setAccessToken(accessTokenValue);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setAccessToken(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, accessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
