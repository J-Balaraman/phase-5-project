from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-workout_routines', '-password')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active_workout_id = db.Column(db.Integer)

    workout_routines = db.relationship(
        'WorkoutRoutine',
        secondary='user_workout_routine',
        back_populates='users'
    )
    exercise_logs = db.relationship('ExerciseLog', back_populates='user', lazy=True)
    user_metrics = db.relationship('UserMetrics', back_populates='user', lazy=True)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address and address.endswith('.com'), "Invalid email format"
        return address

    @validates('username')
    def validate_username(self, key, username):
        assert username is not None and len(username) > 0, "Username cannot be empty"
        return username

class WorkoutRoutine(db.Model, SerializerMixin):
    __tablename__ = 'workout_routines'

    serialize_rules = ('-user_workout_routine')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

    user = db.relationship('User', back_populates='exercise_logs')

class UserMetrics(db.Model, SerializerMixin):
    __tablename__ = 'user_metrics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float)
    body_fat = db.Column(db.Float)

    user = db.relationship('User', back_populates='user_metrics')

class UserWorkoutRoutine(db.Model, SerializerMixin):
    __tablename__ = 'user_workout_routine'

    serialize_rules = ('-user', '-workout_routine')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    workout_routine_id = db.Column(db.Integer, db.ForeignKey('workout_routines.id'), primary_key=True)
