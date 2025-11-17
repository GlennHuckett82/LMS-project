import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public routes */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />

          {/* Later: add protected routes for courses, lessons, etc. */}
          {/* <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;