import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

function Home() {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Scope</h1>
        <p>Programmer Training</p>
      </header>

      <div className="home-links">
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </div>
    </div>
  );
}

export default Home;