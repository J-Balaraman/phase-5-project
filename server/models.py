from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-user_workout_routine')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active_workout_id = db.Column(db.Integer)

    workout_routines = db.relationship(
        'WorkoutRoutine',
        secondary='user_workout_routine',
        back_populates='users'
    )
    exercise_logs = db.relationship('ExerciseLog', back_populates='user', lazy=True)
    user_metrics = db.relationship('UserMetrics', back_populates='user', lazy=True)

class WorkoutRoutine(db.Model, SerializerMixin):
    __tablename__ = 'workout_routines'

    serialize_rules = ('-user_workout_routine')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sunday = db.Column(db.Text, nullable=False)
    monday = db.Column(db.Text, nullable=False)
    tuesday = db.Column(db.Text, nullable=False)
    wednesday = db.Column(db.Text, nullable=False)
    thursday = db.Column(db.Text, nullable=False)
    friday = db.Column(db.Text, nullable=False)
    saturday = db.Column(db.Text, nullable=False)

    users = db.relationship(
        'User',
        secondary='user_workout_routine',
        back_populates='workout_routines'
    )

class ExerciseLog(db.Model, SerializerMixin):
    __tablename__ = 'exercise_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

class UserMetrics(db.Model, SerializerMixin):
    __tablename__ = 'user_metrics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float)
    body_fat = db.Column(db.Float)

class UserWorkoutRoutine(db.Model, SerializerMixin):
    __tablename__ = 'user_workout_routine'

    serialize_rules = ('-user', '-workout_routine')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    workout_routine_id = db.Column(db.Integer, db.ForeignKey('workout_routines.id'), primary_key=True)

    user = db.relationship('User', back_populates='user_workout_routine')
    workout_routine = db.relationship('WorkoutRoutine', back_populates='user_workout_routine')
