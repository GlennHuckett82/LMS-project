
import React, { useEffect, useState } from "react";
import CourseCard from "../components/CourseCard";
import "../App.css";

// This interface describes the shape of a course object as returned by the API.
// It helps TypeScript catch errors if the data doesn't match what we expect.
interface Course {
  id: number;
  title: string;
  description: string;
  teacher: { id: number; username: string; email: string };
}

// The Dashboard component shows a grid of all available courses.
// It fetches course data from the backend API when the page loads.
const Dashboard: React.FC = () => {
  // State to hold the list of courses.
  const [courses, setCourses] = useState<Course[]>([]);
  // State to track if we're still waiting for data.
  const [loading, setLoading] = useState(true);
  // State to store any error messages from the fetch.
  const [error, setError] = useState<string | null>(null);

  // Fetch course data from the backend when the component mounts.
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/courses/")
      .then((res) => {
        // If the response isn't OK, throw an error so we can show a message.
        if (!res.ok) throw new Error("Failed to fetch courses");
        return res.json();
      })
      .then((data) => {
        // DRF paginates results, so we grab the 'results' array.
        setCourses(data.results);
        setLoading(false);
      })
      .catch((err) => {
        // If something goes wrong, save the error so we can show it to the user.
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Show a loading message while waiting for data.
  if (loading) return <p>Loading courses...</p>;
  // Show an error message if the fetch failed.
  if (error) return <p>Error: {error}</p>;

  // Render the list of courses using CourseCard components.
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