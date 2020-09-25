import os
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine, Numeric, func
from sqlalchemy.sql import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import aggregated
import json

database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()

'''
setup_db(app) : binds flask application and SQLAlchemy
'''
def setup_db(app, database_path=database_path,is_test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    if(is_test==True):
        db.create_all()

'''
Student 
'''
class Student(db.Model):
  __tablename__ = 'students'

  
  userid = Column(String, primary_key=True) # Primary key userid - unique username from the authentication service 
  name = Column(String, nullable=False) # String name of student 
  grade = Column(Integer, nullable=False) # Integer student grade(1-12)
  address = Column(String, nullable=False) #String address
  city = Column(String, nullable=False) #String city
  state = Column(String, nullable=False) #String state
  
  ''' init function '''
  def __init__(self, userid, name, grade, address, city, state):
    self.userid = userid
    self.name = name
    self.grade = grade
    self.address = address
    self.city = city
    self.state = state
  
  '''
  insert(): inserts a new model into a database
  Example usage:
                student = Student(userid=userid, name=name, grade=grade, address=address, city=city, state=state)
                student.insert()
  '''  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  updates(): updates an existing model in database
  Example usage:
                student = Student.query.filter(Student.userid=userid).one_or_none()
                student.userid=userid
                ...
                student.state=state
                student.update()
  '''    
  def update(self):
    db.session.commit()

  '''
  delete(): deletes an existing model from database
  Example usage:
                student = Student.query.filter(Student.userid=userid).one_or_none()
                student.delete()
  ''' 
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the student model with all the entities
  '''
  def format(self):
    return {
        'id'      : self.userid,
        'name'    : self.name,
        'grade'   : self.grade,
        'address' : self.address,
        'city'    : self.city,
        'state'   : self.state
      }

  '''
  Representation of the student model excluding the address
  '''
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

  userid = Column(String, primary_key=True) # Primary key userid - unique username from the authentication service
  name = Column(String, nullable = False) # String name of mentor
  address = Column(String, nullable=False) # String address of mentor
  city = Column(String, nullable=False) # String city
  state = Column(String, nullable=False) #String state
  qualification = Column(String, nullable=False) #String qualification
  add_qualification = Column(String, nullable=False) #String to represent if the mentor has additional qualification
  is_volunteer = Column(Boolean, default=False) # Boolean value representing if the mentor is willing to volunteer in case a student is in need
  price = Column(Integer) #Price per hour that the mentor charges
  avail_time = Column(String) # Mentor available times as string
  offer_courses = relationship('MentorCourse', backref="my_mentors", cascade="all, delete-orphan", lazy=True) #Courses that the mentor is offering
  feedback = relationship('Feedback', backref='mentor_feedback', cascade="all, delete-orphan", lazy=True) #Student feedback and rating to the mentor

  ''' init function '''
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

  '''
  insert(): inserts a new model into a database
  Example usage:
                mentor = Mentor(userid=userid, name=name, address=address, city=city, state=state, qualification=qualification, 
                add_qualification=add_qualification, price=price, avail_time=avail_time, is_volunteer=is_volunteer)
                mentor.insert()
  '''  
  def insert(self):
    db.session.add(self)
    db.session.commit()
 
  '''
  update(): updates an existing model in database
  Example usage:
                mentor = Mentor.query.filter(Mentor.userid=userid).one_or_none()
                mentor.userid=userid
                ...
                mentor.state=state
                mentor.update()
  '''  
  def update(self):
    db.session.commit()

  '''
  delete(): deletes an existing model from database
  Example usage:
                mentor = Mentor.query.filter(Mentor.userid=userid).one_or_none()
                mentor.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the mentor model with all the entities
  '''
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
  
  '''
  Representation of the mentor model excluding the address
  '''
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


'''
MentorCourse: Represents courses offerred by mentor
'''
class MentorCourse(db.Model):
  __tablename__ = 'mentor_courses'

  id = Column(Integer, primary_key=True)  # autoincrementing, unique primary key
  name = Column(String, nullable = False) # String name of the course
  grade = Column(Integer, nullable=False) # Integer grade for which this course is offered (1-12)
  mentor_id = Column(String, ForeignKey('mentors.userid'), nullable=False) # Foreign Key mentor_id

  ''' init function '''
  def __init__(self, name, grade, mentor_id):
    self.name = name
    self.grade = grade
    self.mentor_id = mentor_id
  
  '''
  insert(): inserts a new model into a database
  Example usage:
                course = MentorCourse(name=name, grade=grade, mentor_id=mentor_id)
                course.insert()
  ''' 
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  update(): updates an existing model in database
  Example usage:
                course = MentorCourse.query.filter(MentorCourse.id=id).one_or_none()
                course.name=name
                course.grade=grade
                course.mentor_id=mentor_id
                course.update()
  '''   
  def update(self):
    db.session.commit()

  '''
  delete(): deletes an existing model from database
  Example usage:
                course = MentorCourse.query.filter(MentorCourse.id=id).one_or_none()
                course.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the mentor_courses model
  '''
  def format(self):
    return {
        'id'       : self.id,
        'name'     : self.name,
        'grade'    : self.grade,
        'mentor_id': self.mentor_id
      }

'''
MentorStudentPair: Represents a model which indicates if a mentor is tutoring a student or has tutored a student
'''
class MentorStudentPair(db.Model):
  __tablename__ = 'mentor_student_pairs'

  id = Column(Integer, primary_key=True) # autoincrementing, unique primary key 
  mentorship_year = Column(String)       # String mentorship year, this is a string beacause there can be multiple different years
  present_student = Column(Boolean, nullable=False) # Boolean: if tutoring currently
  mentor_id = Column(String, ForeignKey(Mentor.userid, ondelete='SET NULL'), nullable=True)# Foreign Key mentor's userid
  student_id = Column(String, ForeignKey(Student.userid, ondelete='SET NULL'), nullable=True)# Foreign Key student's userid
  course_id = Column(Integer, ForeignKey(MentorCourse.id, ondelete='SET NULL'), nullable=True) # Foreign Key course id

  '''Init function'''
  def __init__(self, mentorship_year, present_student, mentor_id, student_id, course_id): 
    self.mentorship_year = mentorship_year
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.course_id = course_id
    self.present_student = present_student
  
  '''
  insert(): inserts a new model into a database
  Example usage:
                accept_new_student = MentorStudentPair(mentorship_year=mentorship_year, present_student=present_student, 
                                                       mentor_id=mentor_id, student_id=student_id, course_id=course_id)
                accept_new_student.insert()
  '''  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  update(): updates an existing model in database
  Example usage:
                update_student = MentorStudentPair.query.filter(MentorStudentPair.id=id).one_or_none()
                MentorStudentPair.mentorship_year=mentorship_year
                ...                                         
                update_student.update()
  '''   
  def update(self):
    db.session.commit()

  '''
  delete(): deletes an existing model from database
  Example usage:
                delete_student = MentorStudentPair.query.filter(MentorStudentPair.id=id).one_or_none()
                delete_student.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the model
  '''
  def format(self):
    return {
        'id' : self.id,
        'mentorship_year': self.mentorship_year,
        'mentor_id': self.mentor_id,
        'student_id': self.student_id,
        'course_id': self.course_id,
        'present_student': self.present_student
      }


'''
Feedback: Represents a model which captures student feedback to mentor 
'''
class Feedback(db.Model):
  __tablename__ = 'feedbacks'

  id = Column(Integer, primary_key=True)  # autoincrementing, unique primary key 
  rating = Column(Integer, nullable=False, default=5) #Integer rating (0-5)
  message = Column(String) #Feedback message string
  mentor_id = Column(String, ForeignKey(Mentor.userid, ondelete='SET NULL'), nullable=True) #foreign key mentor id
  student_id = Column(String, ForeignKey(Student.userid, ondelete='SET NULL'), nullable=True) #foreign key student id

  '''init function'''
  def __init__(self, mentor_id, student_id, rating, message):
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.rating = rating
    self.message = message

  '''
  insert(): inserts a new model into a database
  Example usage:
                new_feedback = Feedback(rating=rating, message=message, mentor_id=mentor_id, student_id=student_id)
                new_feedback.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  update(): updates an existing model in database: not used currently
  Example usage:
                update_feedback = Feedback.query.filter(Feedback.id=id).one_or_none()
                update_feedback.mentorship_year=mentorship_year
                ...
                update_feedback.update()
  '''    
  def update(self):
    db.session.commit()
  
  '''
  delete(): deletes an existing model from database
  Example usage:
                delete_feedback = Feedback.query.filter(Feedback.id=id).one_or_none()
                delete_feedback.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the model: excludes stuent id so that feedback remains anonymous
  '''
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

'''
Feedback: Represents a model which captures student messages to mentor 
'''
class RequestMessage(db.Model):
  __tablename__ = 'request_messages'

  id = Column(Integer, primary_key=True) # autoincrementing, unique primary key 
  mentor_id = Column(String, ForeignKey(Mentor.userid, ondelete='SET NULL'), nullable=True) #Foreign key mentor_id
  student_id = Column(String, ForeignKey(Student.userid, ondelete='SET NULL'), nullable=True) #Foreign Key student_id
  course_id = Column(Integer, ForeignKey(MentorCourse.id, ondelete='SET NULL'), nullable=True) #Foreign key couse_id
  message = Column(String) # String message from student
  needs_volunteer = Column(Boolean, default=False) # Boolean representing if the student is in need

  '''init function'''
  def __init__(self, mentor_id, student_id, course_id, message, needs_volunteer):
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.course_id = course_id   
    self.message = message
    self.needs_volunteer = needs_volunteer

  '''
  insert(): inserts a new model into a database
  Example usage:
                message = RequestMessage(mentor_id=mentor_id, student_id=student_id, course_id=course_id, message=message, needs_volunteer=needs_volunteer)
                message.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  delete(): deletes an existing model from database
  Example usage:
                message = RequestMessage.query.filter(RequestMessage.id=id).one_or_none()
                message.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the model
  '''
  def format(self):
    return {
        'id' : self.id,
        'mentor_id': self.mentor_id,
        'student_id': self.student_id,
        'course_id': self.course_id,
        'message' : self.message,
        'needs_volunteer' : self.needs_volunteer
      }
 
'''
ReplyMessage: Represents a model which captures mentor messages to student
''' 
class ReplyMessage(db.Model):
  __tablename__ = 'reply_messages'

  id = Column(Integer, primary_key=True) # autoincrementing, unique primary key 
  mentor_id = Column(String, ForeignKey('mentors.userid', ondelete='SET NULL'), nullable=True)#Foreign key mentor_id
  student_id = Column(String, ForeignKey('students.userid', ondelete='SET NULL'), nullable=True)#Foreign Key student_id
  course_id = Column(Integer, ForeignKey('mentor_courses.id', ondelete='SET NULL'), nullable=True)#Foreign key couse_id
  message = Column(String)
  
  '''init function'''
  def __init__(self, mentor_id, student_id, course_id, message):
    self.mentor_id = mentor_id
    self.student_id = student_id
    self.course_id = course_id   
    self.message = message  

  '''
  insert(): inserts a new model into a database
  Example usage:
                message = ReplyMessage(mentor_id=mentor_id, student_id=student_id, course_id=course_id, message=message)
                message.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  '''
  delete(): deletes an existing model from database
  Example usage:
                message = ReplyMessage.query.filter(ReplyMessage.id=id).one_or_none()
                message.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the model
  '''
  def format(self):
    return {
        'id' : self.id,
        'mentor_id': self.mentor_id,
        'student_id': self.student_id,
        'course_id': self.course_id,
        'message' : self.message
      }   

'''
AdminMessage: Represents a model which captures mentor and student messages to Admin
''' 
class AdminMessage(db.Model): 
  __tablename__ = 'admin_messages'

  id = Column(Integer, primary_key=True) # autoincrementing, unique primary key 
  mentor_id = Column(String, ForeignKey('mentors.userid', ondelete='SET NULL'), nullable=True) #Foreign Key mentor_id
  student_id = Column(String, ForeignKey('students.userid', ondelete='SET NULL'), nullable=True)#Foreign Key student_id
  message = Column(String) #String message to Admin

  '''init function'''
  def __init__(self, message, student_id, mentor_id):
    self.message = message
    if student_id!=None:
      self.student_id = student_id
    if mentor_id!=None:
      self.mentor_id = mentor_id
 
  '''
  insert(): inserts a new model into a database
  Example usage:
                message = AdminMessage(mentor_id=mentor_id, student_id=student_id, message=message)
                message.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  delete(): deletes an existing model from database
  Example usage:
                message = AdminMessage.query.filter(AdminMessage.id=id).one_or_none()
                message.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  Representation of the model
  '''
  def format(self):
    return {
        'id' : self.id,
        'mentor_id': self.mentor_id,
        'student_id': self.student_id,
        'message' : self.message
      }
