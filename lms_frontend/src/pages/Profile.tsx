import React, { useCallback, useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { Link } from "react-router-dom";
import "../App.css";
import api from '../services/api';

// Student profile page: shows all courses, highlights which ones you’re enrolled in,
// lets you enroll, and opens lessons per course. Written to be easy to trace step-by-step.

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

  // Fetch all courses (without lessons) so we can render the catalog.
  const fetchCourses = useCallback(async () => {
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
  }, []);

  // Fetch lessons once we know which courses are enrolled; supports array or paginated responses.
  const fetchLessonsForCourses = useCallback(async (courseIds: number[]) => {
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
  }, []);

  // Fetch the courses this user is enrolled in so we can show the right buttons/state.
  const fetchEnrollments = useCallback(async () => {
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
  }, [fetchLessonsForCourses]);

  // Enroll in a course and then refresh enrollments + course list so the UI updates.
  const handleEnroll = async (courseId: number) => {
    setEnrolling(courseId);
    try {
      await api.post(`/enrollments/courses/${courseId}/enroll/`);
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
    // Initial load: get courses and enrollments. Also refresh when tab regains focus so data stays fresh.
    fetchCourses();
    fetchEnrollments();
    const onFocus = () => {
      fetchCourses();
      fetchEnrollments();
    };
    window.addEventListener('focus', onFocus);
    return () => {
      window.removeEventListener('focus', onFocus);
    };
  }, [fetchCourses, fetchEnrollments]);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2 className="heading-xl">My Profile</h2>
        <button
          className="button"
          onClick={() => { logout(); window.location.href = "/"; }}
        >
          Logout
        </button>
      </div>
      {loading ? (
        <p>Loading courses...</p>
      ) : error ? (
        <p className="text-error-simple">{error}</p>
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
                  <div className="course-card-actions">
                    <button
                      className="button"
                      onClick={() => setOpenDropdown(openDropdown === course.id ? null : course.id)}
                      disabled={!isEnrolled}
                    >
                      View Lessons
                    </button>
                    {!isEnrolled && (
                      <button
                        className="button button-enroll-primary"
                        onClick={() => handleEnroll(course.id)}
                        disabled={enrolling === course.id}
                      >
                        {enrolling === course.id ? 'Enrolling...' : 'Enroll'}
                      </button>
                    )}
                  </div>
                  {isEnrolled && openDropdown === course.id && (
                    <div className="lessons-panel">
                      <ul className="lessons-list">
                        {lessons.length === 0 ? (
                          <li className="lessons-list-item">No lessons available.</li>
                        ) : (
                          lessons.map((lesson) => (
                            <li key={lesson.id} className="lessons-list-item-spaced">
                              {lesson.is_completed && <span className="lesson-complete-icon">✓</span>}
                              <span className="lesson-title-text">{lesson.title}</span>
                              <Link
                                to={`/lessons/${lesson.id}`}
                                className="lesson-link-subtle"
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
          <div className="profile-cta">
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