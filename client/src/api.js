import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});

export const login = (email, password) => api.post('/login', { email, password });
export const register = (username, email, password) => api.post('/register', { username, email, password });
export const getDashboard = () => api.get('/dashboard');
export const getWorkouts = () => api.get('/workouts');
export const getWorkoutDetails = (id) => api.get(`/workouts/${id}`);
export const createWorkout = (workout) => api.post('/workouts', workout);
export const getExerciseLogs = () => api.get('/exercise_logs');
export const getUserMetrics = () => api.get('/user_metrics');
