from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
database_path = "postgres://{}/{}".format('anusharavilla:SriSha1234@localhost:5432', database_name) # TODO: Change here before testing

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Student
'''

class Student(db.Model):
  __tablename__ = 'students'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  grade = Column(Integer, nullable=False)
  address = Column(String, nullable=False)
  city = Column(String, nullable=False)
  state = Column(String, nullable=False)
  rating = Column(Integer)
  
  def __init__(self, name, grade, address, city, state, rating):
    self.name = name
    self.grade = grade
    self.address = address
    self.city = city
    self.state = state
    self.rating = rating

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
        'id'     : self.id,
        'name'   : self.name,
        'address': self.address,
        'city'   : self.city,
        'state'  : self.state,
        'rating' : self.rating
            }


'''
Mentor

'''
class Mentor(db.Model):  
  __tablename__ = 'mentors'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable = False)
  address = Column(String, nullable=False)
  city = Column(String, nullable=False)
  state = Column(String, nullable=False)
  rating = Column(Integer)
  qualification = Column(String, nullable=False)
  add_qualification = Column(String, nullable=False)
  isVolunteer = Column(Boolean, default=False)
  price = Column(Integer)
  ## available time and available subjects

  def __init__(self, name, address, city, state, rating, qualification, add_qualification, isVolunteer, price):
    self.name = name
    self.address = address
    self.city = city
    self.state = state
    self.rating = rating
    self.qualification = qualification
    self.add_qualification = add_qualification
    self.isVolunteer = isVolunteer
    self.price = price


  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id'               : self.id,
      'name'             : self.name,
      'address'          : self.address,
      'city'             : self.city,
      'state'            : self.state,
      'rating'           : self.rating,
      'qualification'    : self.qualification,
      'add_qualification': self.add_qualification,
      'isVolunteer'      : self.isVolunteer,
      'price'            : self.price
    }


class Feedback(db.Model):
  __tablename__ = 'feedbacks'

  id = Column(Integer, primary_key=True)
  isMentorFeedback = Column(Boolean, nullable=False)
  mentor_id = Column(Integer, nullable=False)
  student_id = Column(Integer, nullable=False) 
  rating = Column(Integer, nullable=False, default=5)
  message = Column(String)

  def __init__(self, isMentorFeedback, mentor_id, student_id, rating, message):
    self.isMentorFeedback = isMentorFeedback
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.rating = rating
    self.message = message

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id'              : self.id,
      'isMentorFeedback': self.isMentorFeedback,
      'mentor_id'       : self.mentor_id,
      'student_id'      : self.student_id,
      'rating'          : self.rating,
      'message'         : self.message 
    }





