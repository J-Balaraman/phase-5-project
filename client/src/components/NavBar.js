import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/register">Register</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/workouts">Workouts</Link></li>
        <li><Link to="/create_workout">Create Workout</Link></li>
        <li><Link to="/user_logs">Logs</Link></li>
        <li><Link to="/user_graphs">User Graphs</Link></li>
      </ul>
    </nav>
  );
}

export default NavBar;
