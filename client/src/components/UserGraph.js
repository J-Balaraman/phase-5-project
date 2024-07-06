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

  useEffect(() => {
    axios.get('/user_metrics')
      .then(response => setMetrics(response.data))
      .catch(error => console.error('Error fetching metrics', error));
  }, []);

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
    </div>
  );
};

export default UserGraph;
