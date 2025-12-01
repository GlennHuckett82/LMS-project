import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

const courses = [
  {
    title: "Introduction to Python",
    description:
      "Build a rock-solid foundation in the world's most versatile programming language. From basic syntax to real-world scripts.",
    tag: "Beginner Friendly",
    tagClass: "course-card__tag--beginner",
  },
  {
    title: "Front-End with React",
    description:
      "Go beyond static websites. Learn to build beautiful, fast, and interactive user interfaces with the industry-standard library.",
    tag: "Front-End",
    tagClass: "course-card__tag--frontend",
  },
  {
    title: "Data Structures & Algorithms",
    description:
      "Master the fundamental concepts that power all software. A crucial step for acing technical interviews and writing efficient code.",
    tag: "Core Concepts",
    tagClass: "course-card__tag--core",
  },
  {
    title: "Modern Databases",
    description:
      "Learn how to design, manage, and query the databases that are the backbone of modern applications, from SQL to NoSQL.",
    tag: "Back-End",
    tagClass: "course-card__tag--backend",
  },
  {
    title: "DevOps Fundamentals",
    description:
      "Bridge the gap between development and operations. Learn the essentials of automation, cloud deployment, and CI/CD pipelines.",
    tag: "Advanced",
    tagClass: "course-card__tag--advanced",
  },
];

function Courses() {
  return (
    <div className="courses-page-wrapper">
      <section className="featured-courses">
        <div className="featured-courses__grid">
          {courses.map((course, idx) => (
            <div className="course-card" key={idx}>
              <div className={`course-card__tag ${course.tagClass}`}>{course.tag}</div>
              <h3 className="course-card__title">{course.title}</h3>
              <p className="course-card__desc">{course.description}</p>
            </div>
          ))}
        </div>
      </section>
      <section className="why-scope">
        <div className="why-scope__header">
          <h2 className="why-scope__title">A Smarter Way to Learn</h2>
          <p className="why-scope__subtitle">We've built our platform around the principles that matter most for your success.</p>
        </div>
        <div className="why-scope__grid">
          <div className="why-scope__item">
            <div className="why-scope__icon">🔧</div>
            <h3 className="why-scope__item-title">Learn by Building</h3>
            <p className="why-scope__item-text">Theory is important, but practical skill is essential. Every course is packed with hands-on projects that mirror the work you'll do as a professional developer.</p>
          </div>
          <div className="why-scope__item">
            <div className="why-scope__icon">🧑‍🏫</div>
            <h3 className="why-scope__item-title">Expert-Led Instruction</h3>
            <p className="why-scope__item-text">Your instructors aren't just teachers; they're seasoned industry veterans from top tech companies who bring real-world context to every lesson.</p>
          </div>
          <div className="why-scope__item">
            <div className="why-scope__icon">🧭</div>
            <h3 className="why-scope__item-title">Career-Focused Curriculum</h3>
            <p className="why-scope__item-text">We don't just teach you to code. We teach you the skills, tools, and best practices that employers are actively looking for right now.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Courses;
