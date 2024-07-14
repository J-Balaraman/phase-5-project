import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { NavLink } from 'react-router-dom';
import AuthContext from './AuthContext';

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const [activeWorkout, setActiveWorkout] = useState(null);
  const [workoutRoutines, setWorkoutRoutines] = useState([]);
  const [userMetrics, setUserMetrics] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/dashboard');
        const userData = response.data;
        setActiveWorkout(userData.active_workout);
        setWorkoutRoutines(userData.workout_routines || []);
        setUserMetrics(userData.user_metrics || []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Error fetching dashboard data. Please try again later.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (!user) {
    return <p>You are not logged in. Please log in to view your dashboard.</p>;
  }

  const { username, email } = user;
  const latestMetric = userMetrics.length > 0 ? userMetrics[userMetrics.length - 1] : null;

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p><strong>Username:</strong> {username}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Active Workout:</strong> {activeWorkout ? activeWorkout : 'No Active Workout'}</p>
      <div>
        <h2 className="text-xl font-bold mb-2">Workout Routines</h2>
        {workoutRoutines.length === 0 ? (
          <p>No workout routines available.</p>
        ) : (
          <ul>
            {workoutRoutines.map(routine => (
              <li key={routine.id}>
                <NavLink to={`/workouts/${routine.id}`}>
                    {routine.name}
                </NavLink>
              </li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h2 className="text-xl font-bold mb-2">User Metrics</h2>
        {userMetrics.length === 0 ? (
          <p>No user metrics available.</p>
        ) : (
          <p>{`Latest Metric: Date - ${latestMetric.date}, Weight - ${latestMetric.weight}, Body Fat - ${latestMetric.body_fat}`}</p>
        )}
      </div>
      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
};

export default Dashboard;
