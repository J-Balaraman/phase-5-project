import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const UserGraph = () => {
  const [metrics, setMetrics] = useState([]);
  const [newMetric, setNewMetric] = useState({ date: '', weight: '', body_fat: '' });

  useEffect(() => {
    axios.get('/user_metrics', {
      headers: { 'x-access-token': localStorage.getItem('token') }
    })
      .then(response => setMetrics(response.data))
      .catch(error => console.error('Error fetching metrics', error));
  }, []);

  const handleChange = (e) => {
    setNewMetric({ ...newMetric, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/user_metrics', newMetric, {
      headers: { 'x-access-token': localStorage.getItem('token') }
    })
      .then(response => {
        const updatedMetrics = [...metrics, response.data];
        setMetrics(updatedMetrics);
        setNewMetric({ date: '', weight: '', body_fat: '' });
      })
      .catch(error => console.error('Error submitting new metric', error));
  };

//  const handleDelete = (id) => {
//    axios.delete('/user_metrics', { data: { id } }, {
//        headers: { 'x-access-token': localStorage.getItem('token') }
//    })
//    .then(response => {
//        setMetrics(metrics.filter(metric => metric.id !== id));
//    })
//    .catch(error => console.error('Error deleting metric', error));
//};



  const weightData = {
    labels: metrics.length ? metrics.map(metric => metric.date) : [],
    datasets: [
      {
        label: 'Weight',
        data: metrics.length ? metrics.map(metric => metric.weight) : [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      }
    ],
  };

  const bodyFatData = {
    labels: metrics.length ? metrics.map(metric => metric.date) : [],
    datasets: [
      {
        label: 'Body Fat',
        data: metrics.length ? metrics.map(metric => metric.body_fat) : [],
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
      }
    ],
  };

  /* <button onClick={() => handleDelete(metric.id)} className="ml-2 px-2 py-1 bg-red-500 text-white rounded">Delete</button> */

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">User Metrics Graph</h2>
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2">Weight</h3>
        <Line data={weightData} />
      </div>
      <div>
        <h3 className="text-lg font-semibold mb-2">Body Fat</h3>
        <Line data={bodyFatData} />
      </div>
      <form onSubmit={handleSubmit} className="mt-8">
        <div className="mb-4">
          <label className="block text-gray-700">Date</label>
          <input type="date" name="date" value={newMetric.date} onChange={handleChange} className="w-full p-2 border" />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Weight</label>
          <input type="number" name="weight" value={newMetric.weight} onChange={handleChange} className="w-full p-2 border" />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Body Fat</label>
          <input type="number" name="body_fat" value={newMetric.body_fat} onChange={handleChange} className="w-full p-2 border" />
        </div>
        <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
      </form>
      <h3 className="text-lg font-semibold mt-8 mb-2">Metric List</h3>
      <ul>
        {metrics.map(metric => (
          <li key={metric.id}>
            Date: {metric.date}, Weight: {metric.weight}, Body Fat: {metric.body_fat}

          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserGraph;
