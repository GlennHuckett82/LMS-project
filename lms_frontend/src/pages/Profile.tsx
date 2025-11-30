import React, { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { Link } from "react-router-dom";
import "../App.css";
import api from '../services/api';

interface Lesson {
  id: number;
  title: string;
  is_completed: boolean;
}

interface Course {
  id: number;
  title: string;
  description: string;
  lessons: Lesson[];
}

interface Enrollment {
  course: {
    id: number;
  };
}

const Profile: React.FC = () => {
  const { logout } = useAuth();

  const [courses, setCourses] = useState<Course[]>([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState<number[]>([]);
  const [courseLessons, setCourseLessons] = useState<{ [courseId: number]: Lesson[] }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDropdown, setOpenDropdown] = useState<number | null>(null);
  const [enrolling, setEnrolling] = useState<number | null>(null);

  // Fetch all courses (no lessons attached)
  const fetchCourses = async () => {
    try {
      const res = await api.get('/courses/');
      let coursesArray: Course[] = [];
      if (Array.isArray(res.data)) {
        coursesArray = res.data;
      } else if (res.data.results) {
        coursesArray = res.data.results;
      }
      setCourses(coursesArray);
      setLoading(false);
    } catch (err) {
      setError("Failed to fetch courses");
      setLoading(false);
    }
  };

  // Fetch user's enrollments
  const fetchEnrollments = async () => {
    try {
      const res = await api.get('/enrollments/my-enrollments/');
      let enrollmentsArray: Enrollment[] = [];
      if (Array.isArray(res.data)) {
        enrollmentsArray = res.data;
      } else if (res.data.results) {
        enrollmentsArray = res.data.results;
      }
      const ids = enrollmentsArray.map((enrollment: Enrollment) => enrollment.course.id);
      setEnrolledCourseIds(ids);
      // After enrollments are fetched, fetch lessons for enrolled courses
      fetchLessonsForCourses(ids);
    } catch (err) {
      // If enrollments can't be fetched, show nothing
    }
  };

  // Fetch lessons for all enrolled courses
  const fetchLessonsForCourses = async (courseIds: number[]) => {
    try {
      const res = await api.get('/lessons/');
      console.log('res.data:', res.data);
      let lessonsArray: any[] = [];
      if (Array.isArray(res.data)) {
        lessonsArray = res.data;
      } else if (res.data.results) {
        lessonsArray = res.data.results;
      }
      console.log('courseIds:', courseIds);
      console.log('lessonsArray:', lessonsArray);
      // Only keep lessons for enrolled courses
      const lessonsByCourse: { [courseId: number]: Lesson[] } = {};
      courseIds.forEach(id => { lessonsByCourse[id] = []; });
      lessonsArray.forEach((lesson: any) => {
        const courseId = lesson.course.id;
        console.log('lesson courseId:', courseId, 'in courseIds:', courseIds.includes(courseId));
        if (courseIds.length === 0 || courseIds.includes(courseId)) {
          if (!lessonsByCourse[courseId]) lessonsByCourse[courseId] = [];
          lessonsByCourse[courseId].push(lesson);
        }
      });
      console.log('Grouped lessons by course:', lessonsByCourse);
      setCourseLessons(lessonsByCourse);
    } catch (err) {
      console.error('Error fetching lessons:', err);
      setCourseLessons({});
    }
  };

  // Enroll in a course
const handleEnroll = async (courseId: number) => {
  setEnrolling(courseId);
  try {
    await api.post(`/enrollments/courses/${courseId}/enroll/`);
    // Refresh enrollments and courses
    fetchEnrollments();
    fetchCourses();
    setError(null);
  } catch (err: any) {
    setError("Failed to enroll.");
  } finally {
    setEnrolling(null);
  }
};

  useEffect(() => {
    fetchCourses();
    fetchEnrollments();
    window.addEventListener('focus', () => {
      fetchCourses();
      fetchEnrollments();
    });
    return () => {
      window.removeEventListener('focus', fetchCourses);
    };
  }, []);

  return (
    <div className="dashboard-container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h2 style={{ color: "#334e68", fontWeight: 800 }}>My Profile</h2>
        <button
          className="auth-button"
          style={{ width: 'auto', padding: '8px 24px', fontSize: '1rem' }}
          onClick={() => { logout(); window.location.href = "/"; }}
        >
          Logout
        </button>
      </div>
      {loading ? (
        <p>Loading courses...</p>
      ) : error ? (
        <p style={{ color: "#e11d48" }}>{error}</p>
      ) : (
        <>
          <div className="course-grid">
            {courses.map((course) => {
              const isEnrolled = enrolledCourseIds.includes(course.id);
              const lessons = courseLessons[course.id] || [];
              return (
                <div className="course-card" key={course.id}>
                  <h3>{course.title}</h3>
                  <p>{course.description}</p>
                  <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
                    <button
                      className="auth-button"
                      style={{ width: 'auto', padding: '8px 24px', fontSize: '1rem' }}
                      onClick={() => setOpenDropdown(openDropdown === course.id ? null : course.id)}
                      disabled={!isEnrolled}
                    >
                      View Lessons
                    </button>
                    {!isEnrolled && (
                      <button
                        className="auth-button"
                        style={{ width: 'auto', padding: '8px 24px', fontSize: '1rem', background: '#2563eb', color: '#fff' }}
                        onClick={() => handleEnroll(course.id)}
                        disabled={enrolling === course.id}
                      >
                        {enrolling === course.id ? 'Enrolling...' : 'Enroll'}
                      </button>
                    )}
                  </div>
                  {isEnrolled && openDropdown === course.id && (
                    <div style={{ marginTop: "1rem", background: "#f7f9fb", borderRadius: "8px", boxShadow: "0 2px 8px rgba(51, 78, 104, 0.07)", padding: "1rem" }}>
                      <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                        {lessons.length === 0 ? (
                          <li style={{ color: "#334e68", fontWeight: 600 }}>No lessons available.</li>
                        ) : (
                          lessons.map((lesson) => (
                            <li key={lesson.id} style={{ color: "#334e68", fontWeight: 600, marginBottom: "0.5rem" }}>
                              {lesson.is_completed && <span style={{ color: '#22c55e', marginRight: '0.5rem' }}>✓</span>}
                              <span style={{ textDecoration: 'none', color: '#334e68', fontWeight: 600, marginRight: '1rem' }}>{lesson.title}</span>
                              <Link
                                to={`/lessons/${lesson.id}`}
                                style={{ marginLeft: "1rem", color: "#486581", fontWeight: 400, textDecoration: "underline" }}
                              >
                                Open Lesson
                              </Link>
                            </li>
                          ))
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              );
            })}
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