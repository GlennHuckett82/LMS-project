import React from "react";

interface CourseCardProps {
  title: string;
  description: string;
  teacher: string;
}

const CourseCard: React.FC<CourseCardProps> = ({ title, description, teacher }) => (
  <div className="course-card">
    <h3>{title}</h3>
    <p>{description}</p>
    <p><strong>Teacher:</strong> {teacher}</p>
  </div>
);

export default CourseCard;