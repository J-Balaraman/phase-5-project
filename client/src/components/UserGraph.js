import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

const UserGraph = () => {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    axios.get('/user_metrics')
      .then(response => setMetrics(response.data))
      .catch(error => console.error('Error fetching metrics', error));
  }, []);

  const data = {
    labels: metrics.map(metric => metric.date),
    datasets: [
      {
        label: 'Weight',
        data: metrics.map(metric => metric.weight),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
      {
        label: 'Body Fat',
        data: metrics.map(metric => metric.body_fat),
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
      },
    ],
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">User Metrics Graph</h2>
      <Line data={data} />
    </div>
  );
};

export default UserGraph;
