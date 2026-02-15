
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
import QuizPage from "./pages/Quiz";
import QuizResultPage from "./pages/QuizResult";
import TeacherDashboard from "./pages/TeacherDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import AdminCoursesOverview from "./pages/AdminCoursesOverview";
import { AuthProvider } from "./auth/AuthContext";
import MainLayout from "./auth/MainLayout";
import RequireAuth from "./auth/RequireAuth";



function App() {
  // Provide authentication context to the entire app
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Public routes wrapped in MainLayout for consistent navigation */}
            <Route element={<MainLayout />}>
              <Route path="/" element={<Home />} />
              <Route path="/courses" element={<Courses />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Route>

            {/* Protected profile route */}
            <Route path="/profile" element={
              <RequireAuth>
                <Profile />
              </RequireAuth>
            } />

            {/* Protected teacher and admin dashboards */}
            <Route path="/teacher-dashboard" element={
              <RequireAuth>
                <TeacherDashboard />
              </RequireAuth>
            } />
            <Route path="/admin-dashboard" element={
              <RequireAuth>
                <AdminDashboard />
              </RequireAuth>
            } />
            <Route path="/admin-courses" element={
              <RequireAuth>
                <AdminCoursesOverview />
              </RequireAuth>
            } />

            {/* Protected lesson detail route */}
            <Route path="/lessons/:lessonId" element={
              <RequireAuth>
                <LessonDetail />
              </RequireAuth>
            } />

            {/* Protected quiz routes */}
            <Route path="/quiz/:lessonId" element={
              <RequireAuth>
                <QuizPage />
              </RequireAuth>
            } />
            <Route path="/quiz/result/:attemptId" element={
              <RequireAuth>
                <QuizResultPage />
              </RequireAuth>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;