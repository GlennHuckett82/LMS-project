import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";   

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Default homepage route */}
          <Route path="/" element={<Home />} />

          {/* Public routes */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />

          {/* Dashboard route */}
          <Route path="/courses" element={<Dashboard />} />

          {/* Later: protected routes for courses, lessons, etc. */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;