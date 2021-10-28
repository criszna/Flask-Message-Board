from flask import Flask
from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__ ='users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.Text,nullable=False)
    date = db.Column(db.String(100),nullable=False)
    category = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(100))

class Inprogress(db.Model):
    __tablename__ = 'inprogress'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.Text,nullable=False)
    date = db.Column(db.String(100),nullable=False)
    category = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(100))

class Done(db.Model):
    __tablename__ = 'done'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.Text,nullable=False)
    date = db.Column(db.String(100),nullable=False)
    category = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(100))
