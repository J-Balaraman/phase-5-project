import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const WorkoutDetails = () => {
  const { id } = useParams();
  const [workout, setWorkout] = useState(null);

  useEffect(() => {
    const fetchWorkout = async () => {
      try {
        const token = localStorage.getItem('token');
        const config = {
          headers: {
            Authorization: `Bearer ${token}`
          }
        };
    
        const response = await axios.get(`/workouts/${id}`, config);
        setWorkout(response.data);
      } catch (error) {
        console.error('Error fetching workout', error);
      }
    };    

    fetchWorkout();
  }, [id]);

  const addWorkoutToUser = async () => {
    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
  
      await axios.post(`/workouts/${id}`, {}, config);
      alert('Workout added successfully');
    } catch (error) {
      console.error('Error adding workout', error);
    }
  };  

  const setActiveWorkout = async () => {
    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
  
      await axios.patch(`/workouts/${id}`, {}, config);
      alert('Workout set as active successfully');
    } catch (error) {
      console.error('Error setting active workout', error);
    }
  };  

  const deleteWorkout = async () => {
    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
  
      await axios.delete(`/workouts/${id}`, config);
      alert('Workout deleted successfully');
    } catch (error) {
      console.error('Error deleting workout', error);
    }
  };  

  if (!workout) {
    return <p></p>;
  }

  const days = [
    { name: "Sunday", exercises: workout.sunday },
    { name: "Monday", exercises: workout.monday },
    { name: "Tuesday", exercises: workout.tuesday },
    { name: "Wednesday", exercises: workout.wednesday },
    { name: "Thursday", exercises: workout.thursday },
    { name: "Friday", exercises: workout.friday },
    { name: "Saturday", exercises: workout.saturday }
  ];

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">{workout.name}</h2>
      <p><strong>Description:</strong> {workout.description}</p>
      <p><strong>Days:</strong></p>
      <ul>
        {days.map((day, index) => (
          <li key={index}>{`${day.name}: ${day.exercises}`}</li>
        ))}
      </ul>
      <button onClick={addWorkoutToUser} className="bg-blue-500 text-white p-2 rounded mt-4">Add Workout</button>
      <button onClick={setActiveWorkout} className="bg-green-500 text-white p-2 rounded mt-4">Set as Active Workout</button>
      <button onClick={deleteWorkout} className="bg-red-500 text-white p-2 rounded mt-4">Delete Workout From Your Library</button>
    </div>
  );
};

export default WorkoutDetails;
