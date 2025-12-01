
// Main application component for the LMS frontend.
// Sets up React Router for navigation between pages.

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
// import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Courses from "./pages/Courses";
import LessonDetail from "./pages/LessonDetail";
import { AuthProvider } from "./auth/AuthContext";
import RequireAuth from "./auth/RequireAuth";



function App() {
  // Provide authentication context to the entire app
  return (
    <AuthProvider>
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


            {/* Protected profile route */}
            <Route path="/profile" element={
              <RequireAuth>
                <Profile />
              </RequireAuth>
            } />

            {/* Protected lesson detail route */}
            <Route path="/lessons/:lessonId" element={
              <RequireAuth>
                <LessonDetail />
              </RequireAuth>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;