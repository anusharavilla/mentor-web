import os
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine, Numeric, func
from sqlalchemy.sql import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import aggregated
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

  userid = Column(String, primary_key=True)
  name = Column(String, nullable=False)
  grade = Column(Integer, nullable=False)
  address = Column(String, nullable=False)
  city = Column(String, nullable=False)
  state = Column(String, nullable=False)
  
  
  def __init__(self, userid, name, grade, address, city, state):
    self.userid = userid
    self.name = name
    self.grade = grade
    self.address = address
    self.city = city
    self.state = state
    
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
        'id'      : self.userid,
        'name'    : self.name,
        'grade'   : self.grade,
        'address' : self.address,
        'city'    : self.city,
        'state'   : self.state
      }

  def format_mentor(self):
    return {
        'id'      : self.userid,
        'name'    : self.name,
        'grade'   : self.grade,
        'city'    : self.city,
        'state'   : self.state
      }


'''
Mentor

'''

class Mentor(db.Model):  
  __tablename__ = 'mentors'

  userid = Column(String, primary_key=True)
  name = Column(String, nullable = False)
  address = Column(String, nullable=False)
  city = Column(String, nullable=False)
  state = Column(String, nullable=False)
  qualification = Column(String, nullable=False)
  add_qualification = Column(String, nullable=False)
  is_volunteer = Column(Boolean, default=False)
  price = Column(Integer)
  avail_time = Column(String)
  offer_courses = relationship('MentorCourse', backref="my_mentors", cascade="all, delete-orphan", lazy=True)
  feedback = relationship('Feedback', backref='mentor_feedback', cascade="all, delete-orphan", lazy=True)


  def __init__(self, userid, name, address, city, state, qualification, add_qualification, price, avail_time, is_volunteer):
    self.userid = userid
    self.name = name
    self.address = address
    self.city = city
    self.state = state
    self.qualification = qualification
    self.add_qualification = add_qualification
    self.is_volunteer = is_volunteer
    self.price = price
    self.avail_time = avail_time

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
        'id'               : self.userid,
        'name'             : self.name,
        'address'          : self.address,
        'city'             : self.city,
        'state'            : self.state,
        'qualification'    : self.qualification,
        'add_qualification': self.add_qualification,
        'isVolunteer'      : self.is_volunteer,
        'price'            : self.price,
        'availTime'        : self.avail_time
      }

  def format_student(self):
    return {
        'id'               : self.userid,
        'name'             : self.name,
        'city'             : self.city,
        'state'            : self.state,
        'qualification'    : self.qualification,
        'add_qualification': self.add_qualification,
        'isVolunteer'      : self.is_volunteer,
        'price'            : self.price,
        'availTime'        : self.avail_time
      }



class MentorCourse(db.Model):
  __tablename__ = 'mentor_courses'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable = False)
  grade = Column(Integer, nullable=False)
  mentor_id = Column(String, ForeignKey('mentors.userid'), nullable=False)

  def __init__(self, name, grade, mentor_id):
    self.name = name
    self.grade = grade
    self.mentor_id = mentor_id

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


class MentorStudentPair(db.Model):
  __tablename__ = 'mentor_student_pairs'

  id = Column(Integer, primary_key=True)  
  mentorship_year = Column(String) 
  present_student = Column(Boolean, nullable=False)
  mentor_id = Column(String, ForeignKey(Mentor.userid, ondelete='SET NULL'), nullable=True)
  student_id = Column(String, ForeignKey(Student.userid, ondelete='SET NULL'), nullable=True)
  course_id = Column(Integer, ForeignKey(MentorCourse.id, ondelete='SET NULL'), nullable=True)

  def __init__(self, mentorship_year, present_student, mentor_id, student_id, course_id): 
    self.mentorship_year = mentorship_year
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.course_id = course_id
    self.present_student = present_student

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
        'mentorship_year': self.mentorship_year,
        'mentor_id': self.mentor_id,
        'student_id': self.student_id,
        'course_id': self.course_id,
        'present_student': self.present_student
      }


class Feedback(db.Model):
  __tablename__ = 'feedbacks'

  id = Column(Integer, primary_key=True)  
  rating = Column(Integer, nullable=False, default=5)
  message = Column(String)
  mentor_id = Column(String, ForeignKey(Mentor.userid, ondelete='SET NULL'), nullable=True)
  student_id = Column(String, ForeignKey(Student.userid, ondelete='SET NULL'), nullable=True)

  def __init__(self, mentor_id, student_id, rating, message):
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
        'mentor_id'       : self.mentor_id,
        'rating'          : self.rating,
        'message'         : self.message 
      }

  def __repr__(self):
    return {
        'id'              : self.id,
        'mentor_id'       : self.mentor_id,
        'rating'          : self.rating,
        'message'         : self.message 
      } 


class RequestMessage(db.Model):
  __tablename__ = 'request_messages'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(String, ForeignKey(Mentor.userid, ondelete='SET NULL'), nullable=True)
  student_id = Column(String, ForeignKey(Student.userid, ondelete='SET NULL'), nullable=True)
  course_id = Column(Integer, ForeignKey(MentorCourse.id, ondelete='SET NULL'), nullable=True)
  message = Column(String)
  needs_volunteer = Column(Boolean, default=False)

  def __init__(self, mentor_id, student_id, course_id, message, needs_volunteer):
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.course_id = course_id   
    self.message = message
    self.needs_volunteer = needs_volunteer


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
        'needs_volunteer' : self.needs_volunteer
      }
 
 
class ReplyMessage(db.Model):
  __tablename__ = 'reply_messages'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(String, ForeignKey('mentors.userid', ondelete='SET NULL'), nullable=True)
  student_id = Column(String, ForeignKey('students.userid', ondelete='SET NULL'), nullable=True)
  course_id = Column(Integer, ForeignKey('mentor_courses.id', ondelete='SET NULL'), nullable=True)
  message = Column(String)

  def __init__(self, mentor_id, student_id, course_id, message):
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.course_id = course_id   
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
        'id' : self.id,
        'mentor_id': self.mentor_id,
        'student_id': self.student_id,
        'course_id': self.course_id,
        'message' : self.message
      }   


class AdminMessage(db.Model): 
  __tablename__ = 'admin_messages'

  id = Column(Integer, primary_key=True)
  mentor_id = Column(String, ForeignKey('mentors.userid', ondelete='SET NULL'), nullable=True)
  student_id = Column(String, ForeignKey('students.userid', ondelete='SET NULL'), nullable=True)
  message = Column(String)

  def __init__(self, message, student_id, mentor_id):
    self.message = message
    if student_id!=None:
      self.student_id = student_id
    if mentor_id!=None:
      self.mentor_id = mentor_id

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
        'message' : self.message
      }
