import os
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
    
def db_drop_and_create_all():
    db.drop_all()
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
  
  def __init__(self, name, grade, address, city, state):
    self.name = name
    self.grade = grade
    self.address = address
    self.city = city
    self.state = state
    self.rating = 5
    
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
        'id'      : self.id,
        'name'    : self.name,
        'address' : self.address,
        'city'    : self.city,
        'state'   : self.state,
        'rating'  : self.rating
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
  availTime = Column(String)
  offerCourses = relationship('Course', backref='mentor_courses', cascade='all, delete-orphan', lazy=True)
  feedback = relationship('Feedback', backref='mentor_feedback', cascade='all, delete-orphan', lazy=True)

  def __init__(self, name, address, city, state, qualification, add_qualification, isVolunteer, price, availTime):
    self.name = name
    self.address = address
    self.city = city
    self.state = state
    self.qualification = qualification
    self.add_qualification = add_qualification
    self.isVolunteer = isVolunteer
    self.price = price
    self.availTime = availTime
    self.rating = 5
    self.feedback = ''


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
      'price'            : self.price,
      'availTime'        : self.availTime,
      'feedback'         : self.feedback
    }

'''
Mentor Courses list
'''
class MentorCourse(db.Model):
  __tablename__ = 'mentor_courses'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable = False)
  grade = Column(Integer, nullable=False)
  mentor_id = Column(Integer, ForeignKey('Mentor.id'), nullable=False)

  def __init__(self, name, grade):
    self.name = name
    self.grade = grade

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
      'id'       : self.id,
      'name'     : self.name,
      'grade'    : self.grade,
      'mentor_id': self.mentor_id
    }


class Feedback(db.Model):
  __tablename__ = 'feedbacks'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(Integer, ForeignKey('Mentor.id', ondelete='SET NULL'), nullable=True)
  rating = Column(Integer, nullable=False, default=5)
  message = Column(String)

  def __init__(self, isMentorFeedback, mentor_id, student_id, rating, message):
    self.mentor_id = mentor_id
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
      'mentor_id'       : self.mentor_id,
      'rating'          : self.rating,
      'message'         : self.message 
    }

## only students can give feedbacks .. make sure randoms can't 


class MentorStudentPair(db.Model):
  __tablename__ = 'mentor_student_pairs'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(Integer, ForeignKey('Mentor.id', ondelete='SET NULL'), nullable=True)
  student_id = Column(Integer, ForeignKey('Student.id', ondelete='SET NULL'), nullable=True)
  present_student = Column(Boolean, nullable=False)
  mentorship_year = Column(Integer)
  course_id = Column(Integer, ForeignKey('MentorCourse.id', ondelete='SET NULL'), nullable=True)

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
      'id' : self.id,
      'mentor_id': self.mentor_id,
      'student_id': self.student_id,
      'present_student': self.present_student,
      'mentorship_year': self.mentorship_year,
      'course_id': self.course_id
    }


class RequestMessage(db.Model):
  __tablename__ = 'request_messages'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(Integer, ForeignKey('Mentor.id', ondelete='SET NULL'), nullable=True)
  student_id = Column(Integer, ForeignKey('Student.id', ondelete='SET NULL'), nullable=True)
  course_id = Column(Integer, ForeignKey('MentorCourse.id', ondelete='SET NULL'), nullable=True)
  message = Column(String)
  needsVolunteer = Column(Boolean, default=False)

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
      'id' : self.id,
      'mentor_id': self.mentor_id,
      'student_id': self.student_id,
      'course_id': self.course_id,
      'message' : self.message,
      'needsVolunteer' : self.needsVolunteer
    }

  ## after mentor clicks accept key, delete the message automatically and send reply message

class ReplyMessage(db.Model):
  __tablename__ = 'reply_messages'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(Integer, ForeignKey('Mentor.id', ondelete='SET NULL'), nullable=True)
  student_id = Column(Integer, ForeignKey('Student.id', ondelete='SET NULL'), nullable=True)
  course_id = Column(Integer, ForeignKey('MentorCourse.id', ondelete='SET NULL'), nullable=True)
  message = Column(String)

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
      'id' : self.id,
      'mentor_id': self.mentor_id,
      'student_id': self.student_id,
      'course_id': self.course_id,
      'message' : self.message
    }
  
  ## if student is accepted sent accept message, rejected, send reject message, when done button is clicked, delete message



