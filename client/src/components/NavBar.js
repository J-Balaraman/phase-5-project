import React, { useContext } from 'react';
import { Link, useHistory } from 'react-router-dom';
import AuthContext from './AuthContext';

const NavBar = () => {
  const { user, logout } = useContext(AuthContext);
  const history = useHistory();

  const handleLogout = () => {
    logout();
    history.push('/login');
  };

  return (
    <nav className="p-4 bg-gray-800 text-white flex justify-between">
      <ul className="flex space-x-4">
        <li><Link to="/">Home</Link></li>
        {user ? (
          <>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/workouts">Workouts</Link></li>
            <li><Link to="/create_workout">Create Workout</Link></li>
            <li><Link to="/user_logs">Logs</Link></li>
            <li><Link to="/user_metrics">User Graphs</Link></li>
            <li><button onClick={handleLogout}>Logout</button></li>
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
