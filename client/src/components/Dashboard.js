import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import AuthContext from './AuthContext';

const Dashboard = () => {
  const { user, loading } = useContext(AuthContext);
  const [activeWorkout, setActiveWorkout] = useState(null);
  const [workoutRoutines, setWorkoutRoutines] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        if (user) {
          const response = await axios.get('/dashboard');
          setActiveWorkout(response.data.active_workout);
          setWorkoutRoutines(response.data.workout_routines);
        }
      } catch (error) {
        console.error('Error fetching dashboard data', error);
      }
    };

    fetchDashboardData();
  }, [user]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!user) {
    return <p>You are not logged in. Please log in to view your dashboard.</p>;
  }

  const { username, email, user_metrics } = user;
  const latest_metric = user_metrics.length > 0 ? user_metrics[user_metrics.length - 1] : null;

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p><strong>Username:</strong> {username}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Active Workout:</strong> {activeWorkout || 'None'}</p>
      <div>
        <h2 className="text-xl font-bold mb-2">Workout Routines</h2>
        {workoutRoutines.length === 0 ? (
          <p>No workout routines available.</p>
        ) : (
          <ul>
            {workoutRoutines.map(routine => (
              <li key={routine.id}>{routine.name}</li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h2 className="text-xl font-bold mb-2">User Metrics</h2>
        {user_metrics.length === 0 ? (
          <p>No user metrics available.</p>
        ) : (
          <li>{`Date: ${latest_metric.date}, Weight: ${latest_metric.weight}, Body Fat: ${latest_metric.body_fat}`}</li>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
