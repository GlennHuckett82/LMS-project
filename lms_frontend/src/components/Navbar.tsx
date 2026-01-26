// Simple top navigation shared across public pages; highlights current route via location.
import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../App.css";

const Navbar: React.FC = () => {
    const location = useLocation();
    return (
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
                    {location.pathname !== '/' && <li><Link to="/" className={`navbar__link${location.pathname === '/' ? ' navbar__link--active' : ''}`}>Home</Link></li>}
                    <li><Link to="/courses" className={`navbar__link${location.pathname === '/courses' ? ' navbar__link--active' : ''}`}>Courses</Link></li>
                    <li><Link to="/login" className={`navbar__link${location.pathname === '/login' ? ' navbar__link--active' : ''}`}>Login</Link></li>
                    <li><Link to="/register" className={`navbar__link${location.pathname === '/register' ? ' navbar__link--active' : ''}`}>Register</Link></li>
                </ul>
            </nav>
        </header>
    );
};

export default Navbar;
