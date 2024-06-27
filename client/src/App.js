import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBar from './components/NavBar';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Register from './components/Register';
import WorkoutList from './components/WorkoutList';
import WorkoutDetails from './components/WorkoutDetails';
import CreateWorkout from './components/CreateWorkout';
import Logs from './components/Logs';
import UserGraph from './components/UserGraph';
import { AuthProvider } from './components/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <NavBar />
        <div className="container mx-auto">
          <Switch>
            <Route path="/dashboard" component={Dashboard} />
            <Route path="/login" component={Login} />
            <Route path="/register" component={Register} />
            <Route path="/workouts" exact component={WorkoutList} />
            <Route path="/workouts/:id" component={WorkoutDetails} />
            <Route path="/create_workout" component={CreateWorkout} />
            <Route path="/user_logs" component={Logs} />
            <Route path="/user_graphs" component={UserGraph} />
          </Switch>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
