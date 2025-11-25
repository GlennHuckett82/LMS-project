import React, { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import "../App.css";

interface Lesson {
  id: number;
  title: string;
}

interface Course {
  id: number;
  title: string;
  description: string;
  lessons: Lesson[];
}

const Profile: React.FC = () => {
  const { logout } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDropdown, setOpenDropdown] = useState<number | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/courses/?expand=lessons")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch courses");
        return res.json();
      })
      .then((data) => {
        // If lessons are not included, mock one lesson per course
        const coursesWithLessons = data.results.map((course: any) => ({
          ...course,
          lessons: course.lessons && course.lessons.length > 0
            ? course.lessons
            : [{ id: 1, title: "Sample Lesson" }],
        }));
        setCourses(coursesWithLessons);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="dashboard-container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h2 style={{ color: "#334e68", fontWeight: 800 }}>My Profile</h2>
        <button className="auth-button" style={{ width: 'auto', padding: '8px 24px', fontSize: '1rem' }} onClick={() => { logout(); window.location.href = "/"; }}>Logout</button>
      </div>
      {loading ? (
        <p>Loading courses...</p>
      ) : error ? (
        <p style={{ color: "#e11d48" }}>{error}</p>
      ) : (
        <>
          <div className="course-grid">
            {courses.map((course) => (
              <div className="course-card" key={course.id}>
                <h3>{course.title}</h3>
                <p>{course.description}</p>
                <button className="auth-button" style={{ width: 'auto', padding: '8px 24px', fontSize: '1rem' }} onClick={() => setOpenDropdown(openDropdown === course.id ? null : course.id)}>
                  View Lessons
                </button>
                {openDropdown === course.id && (
                  <div style={{ marginTop: "1rem", background: "#f7f9fb", borderRadius: "8px", boxShadow: "0 2px 8px rgba(51, 78, 104, 0.07)", padding: "1rem" }}>
                    <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                      {course.lessons.map((lesson) => (
                        <li key={lesson.id} style={{ color: "#334e68", fontWeight: 600, marginBottom: "0.5rem" }}>{lesson.title}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
          <div style={{ marginTop: '2.5rem', textAlign: 'center', maxWidth: '700px', marginLeft: 'auto', marginRight: 'auto', color: '#334e68', fontSize: '1.15rem', fontWeight: 500 }}>
            <p>
              <strong>Ready to level up?</strong> Every course you see above is a new opportunity to grow your skills and unlock your potential. Dive into lessons, challenge yourself, and remember: every step you take brings you closer to your goals. Stay curious, keep building, and enjoy the journey—your future in tech starts here!
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default Profile;
