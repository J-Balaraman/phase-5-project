import React from 'react';
import { useFormik } from 'formik';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const CreateWorkout = () => {
  const history = useHistory();

  const formik = useFormik({
    initialValues: {
      name: '',
      description: '',
      days: [{ exercises: '' }],
    },
    onSubmit: async (values) => {
      try {
        await axios.post('/workouts', values);
        history.push('/workouts');
      } catch (error) {
        console.error('Error creating workout', error);
      }
    },
  });

  const addDay = () => {
    formik.setFieldValue('days', [...formik.values.days, { exercises: '' }]);
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Create Workout</h2>
      <form onSubmit={formik.handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            name="name"
            onChange={formik.handleChange}
            value={formik.values.name}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Description</label>
          <textarea
            name="description"
            onChange={formik.handleChange}
            value={formik.values.description}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Days</label>
          {formik.values.days.map((day, index) => (
            <div key={index} className="mb-2">
              <textarea
                name={`days.${index}.exercises`}
                onChange={formik.handleChange}
                value={day.exercises}
                className="w-full p-2 border rounded"
              />
            </div>
          ))}
          <button type="button" onClick={addDay} className="p-2 bg-gray-500 text-white rounded">Add Day</button>
        </div>
        <button type="submit" className="w-full p-2 bg-blue-500 text-white rounded">Create</button>
      </form>
    </div>
  );
};

export default CreateWorkout;
