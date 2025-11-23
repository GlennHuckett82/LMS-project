import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../App.css";


function Home() {
  const location = useLocation();
  return (
    <div className="homepage-wrapper">
      <header className="site-header">
        <nav className="navbar">
          <div className="navbar__logo">
            <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="2" width="40" height="40" rx="12" fill="#334e68" />
              <path d="M30 16c0-2.2-2-4-6-4s-6 1.8-6 4c0 2.2 2 3.2 6 4.2 4 .9 6 2 6 4.2 0 2.2-2 4-6 4s-6-1.8-6-4" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span className="navbar__logo-text">Scope</span>
          </div>
          <ul className="navbar__links">
            <li><Link to="/" className={`navbar__link${location.pathname === '/' ? ' navbar__link--active' : ''}`}>Home</Link></li>
            <li><Link to="/courses" className={`navbar__link${location.pathname === '/courses' ? ' navbar__link--active' : ''}`}>Courses</Link></li>
            <li><Link to="/login" className={`navbar__link${location.pathname === '/login' ? ' navbar__link--active' : ''}`}>Login</Link></li>
            <li><Link to="/register" className={`navbar__link${location.pathname === '/register' ? ' navbar__link--active' : ''}`}>Register</Link></li>
          </ul>
        </nav>
      </header>
      <main className="homepage-main">
        <section className="hero">
          <div className="hero__background-gradient"></div>
          <div className="hero__main">
            <div className="hero__content">
              <h1 className="hero__title">Programmer Training</h1>
              <p className="hero__subtitle">Master modern programming skills with hands-on courses, projects, and expert guidance. Start your journey to becoming a professional developer today.</p>
              <Link to="/courses" className="hero__cta-button">View Courses</Link>
            </div>
            <div className="hero__image-container">
              <img src="/undraw_programming_j1zw.svg" alt="Programmer at work" className="hero__image" />
            </div>
          </div>
        </section>

        <section className="featured-courses">
          <div className="featured-courses__header">
            <h2 className="featured-courses__title">Chart Your Course to a Career in Code</h2>
            <p className="featured-courses__subtitle">Whether you're starting from scratch or leveling up, our courses are designed to help you master the most in-demand development skills.</p>
          </div>
          <div className="featured-courses__grid">
            <div className="course-card">
              <div className="course-card__tag course-card__tag--beginner">Beginner Friendly</div>
              <h3 className="course-card__title">Introduction to Python</h3>
              <p className="course-card__desc">Build a rock-solid foundation in the world's most versatile programming language. From basic syntax to real-world scripts.</p>
            </div>
            <div className="course-card">
              <div className="course-card__tag course-card__tag--frontend">Front-End</div>
              <h3 className="course-card__title">Front-End with React</h3>
              <p className="course-card__desc">Go beyond static websites. Learn to build beautiful, fast, and interactive user interfaces with the industry-standard library.</p>
            </div>
            <div className="course-card">
              <div className="course-card__tag course-card__tag--core">Core Concepts</div>
              <h3 className="course-card__title">Data Structures & Algorithms</h3>
              <p className="course-card__desc">Master the fundamental concepts that power all software. A crucial step for acing technical interviews and writing efficient code.</p>
            </div>
            <div className="course-card">
              <div className="course-card__tag course-card__tag--backend">Back-End</div>
              <h3 className="course-card__title">Modern Databases</h3>
              <p className="course-card__desc">Learn how to design, manage, and query the databases that are the backbone of modern applications, from SQL to NoSQL.</p>
            </div>
            <div className="course-card">
              <div className="course-card__tag course-card__tag--advanced">Advanced</div>
              <h3 className="course-card__title">DevOps Fundamentals</h3>
              <p className="course-card__desc">Bridge the gap between development and operations. Learn the essentials of automation, cloud deployment, and CI/CD pipelines.</p>
            </div>
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
      </main>
      <footer className="site-footer">
        <p>&copy; 2025 Scope. All Rights Reserved. | <a href="mailto:info@scope.com">Contact</a> | <a href="#">LinkedIn</a></p>
      </footer>
    </div>
  );
}
  export default Home;