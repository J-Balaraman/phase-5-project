import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [newLog, setNewLog] = useState({ date: '', description: '' });
  const [editLog, setEditLog] = useState(null);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = () => {
    axios.get('/user_logs')
      .then(response => setLogs(response.data))
      .catch(error => console.error('Error fetching logs', error));
  };

  const handleCreate = () => {
    axios.post('/user_logs', newLog)
      .then(response => {
        fetchLogs();
        setNewLog({ date: '', description: '' });
      })
      .catch(error => console.error('Error creating log', error));
  };

  const handleUpdate = (log) => {
    axios.patch('/user_logs', log)
      .then(response => {
        fetchLogs();
        setEditLog(null);
      })
      .catch(error => console.error('Error updating log', error));
  };

  const handleDelete = (id) => {
    axios.delete('/user_logs', { data: { id } })
      .then(response => fetchLogs())
      .catch(error => console.error('Error deleting log', error));
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Exercise Logs</h2>
      
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">Create New Log</h3>
        <input 
          type="date" 
          value={newLog.date} 
          onChange={e => setNewLog({ ...newLog, date: e.target.value })} 
          className="mr-2 p-1 border rounded"
        />
        <input 
          type="text" 
          placeholder="Description" 
          value={newLog.description} 
          onChange={e => setNewLog({ ...newLog, description: e.target.value })} 
          className="mr-2 p-1 border rounded"
        />
        <button onClick={handleCreate} className="p-1 bg-blue-500 text-white rounded">Add Log</button>
      </div>

      <ul>
        {logs.map(log => (
          <li key={log.id} className="mb-2">
            {editLog && editLog.id === log.id ? (
              <div>
                <input 
                  type="date" 
                  value={editLog.date} 
                  onChange={e => setEditLog({ ...editLog, date: e.target.value })} 
                  className="mr-2 p-1 border rounded"
                />
                <input 
                  type="text" 
                  value={editLog.description} 
                  onChange={e => setEditLog({ ...editLog, description: e.target.value })} 
                  className="mr-2 p-1 border rounded"
                />
                <button onClick={() => handleUpdate(editLog)} className="p-1 bg-green-500 text-white rounded">Save</button>
                <button onClick={() => setEditLog(null)} className="p-1 bg-gray-500 text-white rounded ml-2">Cancel</button>
              </div>
            ) : (
              <div>
                {`${log.date} - ${log.description}`}
                <button onClick={() => setEditLog(log)} className="p-1 bg-yellow-500 text-white rounded ml-2">Edit</button>
                <button onClick={() => handleDelete(log.id)} className="p-1 bg-red-500 text-white rounded ml-2">Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Logs;
