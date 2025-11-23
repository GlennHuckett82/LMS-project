import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Courses from "./pages/Courses";

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

          {/* Courses page route */}
          <Route path="/courses" element={<Courses />} />

          {/* Later: protected routes for courses, lessons, etc. */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;