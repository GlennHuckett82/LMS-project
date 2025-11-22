import React, { useEffect, useState } from "react";
import CourseCard from "../components/CourseCard";
import "../App.css";

interface Course {
  id: number;
  title: string;
  description: string;
  teacher: { id: number; username: string; email: string };
}

const Dashboard: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/courses/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch courses");
        return res.json();
      })
      .then((data) => {
        setCourses(data.results); // DRF pagination wraps results
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading courses...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="dashboard-container">
      <h2>Available Courses</h2>
      <div className="course-grid">
        {courses.map((course) => (
          <CourseCard
            key={course.id}
            title={course.title}
            description={course.description}
            teacher={course.teacher.username}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;