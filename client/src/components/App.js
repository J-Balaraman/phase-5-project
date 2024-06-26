import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import WorkoutList from './WorkoutList';
import WorkoutDetails from './WorkoutDetails';
import CreateWorkout from './CreateWorkout';
import Logs from './Logs';
import UserGraph from './UserGraph';
import AuthProvider from './AuthContext';
import NavBar from './NavBar';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <NavBar />
        <Switch>
          <Route path="/register" component={Register} />
          <Route path="/login" component={Login} />
          <Route path="/dashboard" component={Dashboard} />
          <Route path="/workouts" component={WorkoutList} />
          <Route path="/workout/:id" component={WorkoutDetails} />
          <Route path="/create_workout" component={CreateWorkout} />
          <Route path="/user_logs" component={Logs} />
          <Route path="/user_graphs" component={UserGraph} />
        </Switch>
      </Router>
    </AuthProvider>
  );
}

export default App;
