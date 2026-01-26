
// Home page for the LMS frontend. Displays navigation, hero section, featured courses, instructors, and platform highlights.
import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

function Home() {
	return (
		<div className="homepage-wrapper">
			{/* Main content: hero, featured courses, instructors, platform highlights */}
			<main className="homepage-main">
				{/* Hero section with call to action */}
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

				{/* Featured courses section */}
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

				<section className="instructors">
					<div className="instructors__header">
						<h2 className="instructors__title">Learn from Industry Leaders</h2>
						<p className="instructors__subtitle">Our instructors are passionate about sharing their expertise to help you succeed.</p>
					</div>
					<div className="instructors__grid">
						<div className="instructor-card">
							<img src="https://randomuser.me/api/portraits/women/44.jpg" alt="Dr. Anya Sharma" className="instructor-card__photo" />
							<h3 className="instructor-card__name">Dr. Anya Sharma</h3>
							<div className="instructor-card__course">Data Structures & Algorithms</div>
							<p className="instructor-card__bio">With a Ph.D. in Computer Science and 10 years at Google's core algorithm team, Anya has a unique gift for making complex topics feel simple and intuitive.</p>
						</div>
						<div className="instructor-card">
							<img src="https://randomuser.me/api/portraits/men/32.jpg" alt="David Chen" className="instructor-card__photo" />
							<h3 className="instructor-card__name">David Chen</h3>
							<div className="instructor-card__course">Front-End with React</div>
							<p className="instructor-card__bio">A senior front-end engineer at Spotify, David is obsessed with creating beautiful user experiences and has led the development of several major product features.</p>
						</div>
						<div className="instructor-card">
							<img src="https://randomuser.me/api/portraits/women/68.jpg" alt="Maria Rodriguez" className="instructor-card__photo" />
							<h3 className="instructor-card__name">Maria Rodriguez</h3>
							<div className="instructor-card__course">Modern Databases</div>
							<p className="instructor-card__bio">As a database architect who has managed terabytes of data for major financial institutions, Maria teaches you how to build systems that are both powerful and scalable.</p>
						</div>
						<div className="instructor-card">
							<img src="https://randomuser.me/api/portraits/men/76.jpg" alt="Kenji Tanaka" className="instructor-card__photo" />
							<h3 className="instructor-card__name">Kenji Tanaka</h3>
							<div className="instructor-card__course">Introduction to Python</div>
							<p className="instructor-card__bio">A former data scientist at NASA, Kenji believes Python is the ultimate tool for problem-solving. His course is famous for its engaging, real-world examples.</p>
						</div>
						<div className="instructor-card">
							<img src="https://randomuser.me/api/portraits/women/12.jpg" alt="Sarah Jenkins" className="instructor-card__photo" />
							<h3 className="instructor-card__name">Sarah Jenkins</h3>
							<div className="instructor-card__course">DevOps Fundamentals</div>
							<p className="instructor-card__bio">Sarah is a Cloud Infrastructure Engineer who has helped startups scale from zero to millions of users. She is passionate about automation and building resilient systems.</p>
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
			<section className="final-invitation">
				<div className="final-invitation__container">
					<h2 className="final-invitation__headline">Your Future Starts Here.</h2>
					<p className="final-invitation__text">Stop dreaming and start building. Join a community of learners and take the first, most important step on your journey to becoming a professional developer. The skills you learn today will build your tomorrow.</p>
				</div>
			</section>
			<footer className="site-footer">
				<p>&copy; 2025 Scope. All Rights Reserved. | <a href="mailto:info@scope.com">Contact</a> | <a href="https://www.linkedin.com" target="_blank" rel="noreferrer">LinkedIn</a></p>
			</footer>
		</div>
	);
}

export default Home;