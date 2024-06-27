import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from './AuthContext';

const NavBar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="p-4 bg-gray-800 text-white">
      <ul className="flex space-x-4">
        {user ? (
          <>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/workouts">Workouts</Link></li>
            <li><Link to="/create_workout">Create Workout</Link></li>
            <li><Link to="/user_logs">Logs</Link></li>
            <li><Link to="/user_graphs">User Graphs</Link></li>
            <li><button onClick={logout}>Logout</button></li>
          </>
        ) : (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default NavBar;
