import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const WorkoutList = () => {
  const [workouts, setWorkouts] = useState([]);

  useEffect(() => {
    axios.get('/workouts')
      .then(response => setWorkouts(response.data))
      .catch(error => console.error('Error fetching workouts', error));
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Workouts</h2>
      <ul>
        {workouts.map(workout => (
          <li key={workout.id}>
            <Link to={`/workouts/${workout.id}`}>{workout.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WorkoutList;
