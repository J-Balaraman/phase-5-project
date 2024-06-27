import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const WorkoutDetails = () => {
  const { id } = useParams();
  const [workout, setWorkout] = useState(null);

  useEffect(() => {
    axios.get(`/workouts/${id}`)
      .then(response => setWorkout(response.data))
      .catch(error => console.error('Error fetching workout', error));
  }, [id]);

  if (!workout) {
    return <p>Loading...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">{workout.name}</h2>
      <p><strong>Description:</strong> {workout.description}</p>
      <p><strong>Days:</strong></p>
      <ul>
        {workout.days.map((day, index) => (
          <li key={index}>{`Day ${index + 1}: ${day.exercises.join(', ')}`}</li>
        ))}
      </ul>
    </div>
  );
};

export default WorkoutDetails;
