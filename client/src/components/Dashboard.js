import React, { useContext } from 'react';
import AuthContext from './AuthContext';

const Dashboard = () => {
  const { user } = useContext(AuthContext);

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Dashboard</h2>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Current Workout Plan:</strong> {user.active_workout_id ? user.active_workout_id : 'None'}</p>
      <p><strong>Workout Routines:</strong></p>
      <ul>
        {user.workout_routines.map((routine, index) => (
          <li key={index}>{routine}</li>
        ))}
      </ul>
      <p><strong>Exercise Logs:</strong></p>
      <ul>
        {user.exercise_logs.map((log, index) => (
          <li key={index}>{log}</li>
        ))}
      </ul>
      <p><strong>Metrics:</strong></p>
      <ul>
        {user.user_metrics.map((metric, index) => (
          <li key={index}>{`Date: ${metric.date}, Weight: ${metric.weight}, Body Fat: ${metric.body_fat}`}</li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
