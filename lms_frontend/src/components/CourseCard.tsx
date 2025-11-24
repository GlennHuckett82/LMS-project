
// This component displays a single course card with its title, description, and teacher.
// It's designed to be reusable for any course in the LMS frontend.
import React from "react";

// Props expected by CourseCard:
// - title: The name of the course
// - description: A short summary of what the course covers
// - teacher: The name of the teacher for this course
interface CourseCardProps {
  title: string;
  description: string;
  teacher: string;
}


// The CourseCard functional component renders a styled card for a course.
// It shows the course title, description, and teacher in a simple layout.
const CourseCard: React.FC<CourseCardProps> = ({ title, description, teacher }) => (
  <div className="course-card">
    <h3>{title}</h3>
    <p>{description}</p>
    <p><strong>Teacher:</strong> {teacher}</p>
  </div>
);


// Export the component so it can be used throughout the app.
export default CourseCard;