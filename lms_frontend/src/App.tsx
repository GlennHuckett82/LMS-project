
// Main application component for the LMS frontend.
// Sets up React Router for navigation between pages.
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Courses from "./pages/Courses";


function App() {
  // The Router wraps all page routes for navigation
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Homepage route */}
          <Route path="/" element={<Home />} />

          {/* Public authentication routes */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />

          {/* Courses listing route */}
          <Route path="/courses" element={<Courses />} />

          {/* Future: Add protected routes for dashboard, lessons, etc. */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;