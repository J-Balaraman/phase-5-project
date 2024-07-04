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
      sunday: '',
      monday: '',
      tuesday: '',
      wednesday: '',
      thursday: '',
      friday: '',
      saturday: ''
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
          <label className="block text-gray-700">Sunday</label>
          <textarea
            name="sunday"
            onChange={formik.handleChange}
            value={formik.values.sunday}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Monday</label>
          <textarea
            name="monday"
            onChange={formik.handleChange}
            value={formik.values.monday}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Tuesday</label>
          <textarea
            name="tuesday"
            onChange={formik.handleChange}
            value={formik.values.tuesday}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Wednesday</label>
          <textarea
            name="wednesday"
            onChange={formik.handleChange}
            value={formik.values.wednesday}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Thursday</label>
          <textarea
            name="thursday"
            onChange={formik.handleChange}
            value={formik.values.thursday}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Friday</label>
          <textarea
            name="friday"
            onChange={formik.handleChange}
            value={formik.values.friday}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Saturday</label>
          <textarea
            name="saturday"
            onChange={formik.handleChange}
            value={formik.values.saturday}
            className="w-full p-2 border rounded"
          />
        </div>
        <button type="submit" className="w-full p-2 bg-blue-500 text-white rounded">Create</button>
      </form>
    </div>
  );
};

export default CreateWorkout;
