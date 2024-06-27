import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Logs = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get('/user_logs')
      .then(response => setLogs(response.data))
      .catch(error => console.error('Error fetching logs', error));
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Exercise Logs</h2>
      <ul>
        {logs.map(log => (
          <li key={log.id}>{`${log.exercise_name} - ${log.reps} reps - ${log.sets} sets`}</li>
        ))}
      </ul>
    </div>
  );
};

export default Logs;
