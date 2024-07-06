import React, { useContext } from 'react';
import AuthContext from './AuthContext';

const Dashboard = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!user) {
    console.log("User not found, redirecting to login");
    return <p>Broken...</p>;
  }

  const latest_metric = user.user_metrics[user.user_metrics.length - 1];

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Dashboard</h2>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Current Workout Plan:</strong> {user.active_workout_id ? user.active_workout_id : 'None'}</p>
      <p><strong>Workout Routines:</strong></p>
      <ul>
        {user.workout_routines.map((routine, index) => (
          <li key={index}>
            <a href={`/workouts/${routine.id}`} className="text-blue-500 underline">
              {routine.name}
            </a>
          </li>
        ))}
      </ul>
      <p><strong>Latest Metric:</strong></p>
      <li>{`Date: ${latest_metric.date}, Weight: ${latest_metric.weight}, Body Fat: ${latest_metric.body_fat}`}</li>
    </div>
  );
};

export default Dashboard;
