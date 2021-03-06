#!/usr/bin/python
import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db, Student, Mentor, MentorCourse, MentorStudentPair, Feedback, RequestMessage, ReplyMessage, AdminMessage
from sqlalchemy import exc, func

from auth_0.auth import AuthError, requires_auth


################HELPER FUCNTIONS ############################

def op_format(mentor_output_list):
  return_list = []

  for op_list in mentor_output_list:

    return_list.append({
      'mentor_id': op_list.mentor_id,
      'time_available':op_list.time_available,
      'course_id':op_list.course_id,
      'course_name':op_list.course_name      
    })

  return return_list

def return_rating(mentor_id):

  mentor_feedback = Feedback.query.with_entities(func.avg(Feedback.rating)).filter(Feedback.mentor_id==mentor_id).all()
  if mentor_feedback[0][0]==None:
    return 0

  return float(mentor_feedback[0][0])

###################ERROR HANDLING PART1 ######################

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class inputNotSpecifiedError(Error):
    """Raised when input is not given"""
    pass

class resourceNotFoundError(Error):
    """Raised when resource is not found"""
    pass

class exceededFeedbackLimitError(Error):
  """ Rasied when attempted to give more than two feedbacks per account """
  pass

class alreadyExistsError(Error):
  """ Raised if attempted to create an already existing entry in database"""
  pass

class actionNotPermittedError(Error):
  """ Raised if someone other than student attempts to give feedback"""
  pass





def create_app(test_config=None):
  
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  ###################PUBLIC ENDPOINTS###########################

  '''
  Endpoint: GET /courses
        Description:         This method returns the list of all unique courses in the database
        Permission:          no permission required.
        Return Value:        Returns only the name and the grade for each course
        Return data format:  Returns status code 200 and json {"success": True, "courses": courses} where courses is the list of courses 
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/courses', methods=['GET'])
  def f_courses():
    courses = []
    courses_formatted = []
  
    try:
      courses = ( MentorCourse.query
                              .with_entities(MentorCourse.name,MentorCourse.grade)
                              .group_by(MentorCourse.name,MentorCourse.grade)
                              .order_by(MentorCourse.grade.desc())
                              .all() 
                )
  
      return jsonify ({
          'success'  : True,
          'courses'  : courses
          })
  
    except:
      abort(422)
  
  #Basic Public end point
  @app.route('/', methods=['GET'])
  def f_working():
    return jsonify ({
          'success'  : True
          })
  
  ####################STUDENT ENDPOINTS########################


  '''
  Endpoint: POST /student_access
        Description:         This method adds a new student with new information from user into the database, student_id is decoded from jwt
        Permission:          'post:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/student_access', methods=['POST'])
  @requires_auth('post:student')
  def student_new_student(student_id): 

    try:   
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
  
      student = Student.query.filter(Student.userid==student_id).first()
      if student!=None:
        raise alreadyExistsError 
      
      new_student = Student(
                           userid = student_id,
                           name = input_request['name'],
                           grade = input_request['grade'],
                           address = input_request['address'],
                           city = input_request['city'],
                           state = input_request['state']
                           )
  
      new_student.insert()
  
      return jsonify({
         'success' : True
        })
    
    except alreadyExistsError:
      abort(406)
    except inputNotSpecifiedError:
      abort(400)
    except:
      abort(422)


  '''
  Endpoint: GET /student_access
        Description:         This method returns the student information based on the studetn id decoded from jwt
        Permission:          'read:student' permission required.
        Return Value:        Returns Student.format() which contains all inforamtion of student
                             Courses that the student has completed previously as previous courses which is a list of MentorCourse.format()
                             Courses that the student is currently enrolled in as current courses which is a list of MentorCourse.format()                              
        Return data format:  Returns status code 200 and json {"success": True, "student": student, "current_courses": list, "previous_courses": list }  
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/student_access', methods=['GET'])
  @requires_auth('read:student')
  def student_student_info(student_id):
    student_formatted = []
    previous_courses_formatted = []
    current_courses_formatted = []
  
    try:
  
      student = Student.query.filter(Student.userid==student_id).first()
      if student!=None:
        student_formatted = student.format()
  
      previous_courses = MentorStudentPair.query.filter(MentorStudentPair.student_id==student_id, MentorStudentPair.present_student==False).all()
      if previous_courses!=None:
        previous_courses_formatted = [ previous_course.format() for previous_course in previous_courses ]
  
      current_courses = MentorStudentPair.query.filter(MentorStudentPair.student_id==student_id, MentorStudentPair.present_student==True).all()
      if current_courses!=None:
        current_courses_formatted = [ current_course.format() for current_course in current_courses ]
      
      return jsonify ({
          'success'          : True,
          'student'          : student_formatted,
          'current_courses'  : current_courses_formatted,
          'previous_courses' : previous_courses_formatted
          })
  
    except:
      abort(422)
  
  '''
  Endpoint: PATCH /student_access
        Description:         This method updates existing student with new information from user into the database, student_id is decoded from jwt
        Permission:          'update:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/student_access', methods=['PATCH'])
  @requires_auth('update:student')
  def student_update_info(student_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
      
      update_student = Student.query.filter(Student.userid==student_id).one_or_none()
      if update_student is None:
        raise resourceNotFoundError
  
      update_student.name = input_request['name']
      update_student.grade = input_request['grade']
      update_student.address = input_request['address']
      update_student.city = input_request['city']
      update_student.state = input_request['state']
  
      update_student.update()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  
  '''
  Endpoint: DELETE /student_access
        Description:         This method deletes existing student from the database, student_id is decoded from jwt
        Permission:          'delete:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/student_access', methods=['DELETE'])
  @requires_auth('delete:student')
  def student_delete_profile(student_id):
  
    try:
      del_student = Student.query.filter(Student.userid==student_id).one_or_none()
      if del_student==None:
        raise resourceNotFoundError
  
      del_student.delete()
  
      return jsonify({
        'success' : True
      })
  
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  
  
  '''
  Endpoint: POST /student_access/search_mentors
        Description:         This method searches for a mentor with information from student, student_id is decoded from jwt. The mentor's city and state must match the information given by the student 
                             in the form along with the course name the student inputs and also the grade.
        Permission:          'read:student' permission required. 
        Return Value:        The search output will include a list of mentors with the following mentor information: the mentor_id, time_available, grade, course name, course id.
        Return data format:  Returns status code 200 and json {"success": True, "search_output":search_output}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/student_access/search_mentors', methods=['POST'])
  @requires_auth('read:student')
  def student_search_mentors(student_id):
    
    try:
      search_input = request.get_json()
      if search_input==None:
        raise inputNotSpecifiedError
  
      course_name = search_input['course_name']
      city = search_input['city']
      state = search_input['state']
      grade = search_input['grade']
  
      search_query = (  Mentor.query
                              .join(MentorCourse, Mentor.userid==MentorCourse.mentor_id)
                              .with_entities(Mentor.userid.label('mentor_id'),Mentor.avail_time.label('time_available'),MentorCourse.name.label('course_name'),MentorCourse.id.label('course_id'))
                              .filter(func.lower(Mentor.city)==func.lower(city), func.lower(Mentor.state)==func.lower(state) , MentorCourse.grade==grade , func.lower(MentorCourse.name).like('%'+func.lower(course_name)+'%'))
                              .all()
                     )
  
      search_output = op_format(search_query)
      
      return jsonify({
         'success' : True,
         'search_output' : search_output
        })
    
    except inputNotSpecifiedError:
      abort(400)
    except:
      abort(422)
    
  '''
  Endpoint: GET /student_access/mentors/<mentor_id>
        Description:         This method returns the mentor information based on the mentor id decoded from request
        Permission:          'read:student' permission required.
        Return Value:        Returns Mentor.format_student() which contains all non-confidential information of mentor
                             Courses that the mentor offers which is a list of MentorCourse.format()
        Return data format:  Returns status code 200 and json {"success": True, "mentor_details": mentor, "courses": list }  
                             or appropriate status code indicating reason for failure
  '''  
  @app.route('/student_access/mentors/<mentor_id>',methods=['GET'])
  @requires_auth('read:student')
  def student_mentor_info(student_id,mentor_id):
    mentor_formatted = []
    courses_formatted = []
  
    try:
      mentor = Mentor.query.filter(Mentor.userid==mentor_id).first()
      if mentor!=None:
        mentor_formatted = mentor.format_student()
      else:
        raise resourceNotFoundError
          
      courses = MentorCourse.query.filter(MentorCourse.mentor_id==mentor_id).all()
      if len(courses)!=0:
        courses_formatted = [course.format() for course in courses]
  
      return jsonify({
        'success' : True,
        'mentor_details': mentor_formatted,
        'courses':courses_formatted
        })
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  

  '''
  Endpoint: POST /student_access/feedback
        Description:         This method adds a feedback from student to mentor into the database, student_id is decoded from jwt. Mentor_id, rating, feedback message are form inputs form Student.
                             Feedback can only be given by students tutored by mentor. Also, there is a maximum limit of 2 feedbacks per student. 
        Permission:          'post:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''    
  @app.route('/student_access/feedback', methods=['POST']) 
  @requires_auth('post:student')
  def student_feedback(student_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
      
      mentor_found = Mentor.query.filter(Mentor.userid==input_request['mentor_id']).one_or_none()
      if mentor_found==None:
        raise resourceNotFoundError

      can_give_feedback = MentorStudentPair.query.filter(MentorStudentPair.mentor_id==input_request['mentor_id'],MentorStudentPair.student_id==student_id).one_or_none()
      if can_give_feedback ==None:
        raise actionNotPermittedError 
  
      student_feedbacks = Feedback.query.filter(Feedback.mentor_id==input_request['mentor_id'],Feedback.student_id==student_id).all() 
      if len(student_feedbacks)>=2:
        raise exceededFeedbackLimitError
  
      new_feedback = Feedback( 
                               mentor_id=input_request['mentor_id'],
                               rating=input_request['rating'],
                               message=input_request['message'],
                               student_id=student_id
                               )
      new_feedback.insert()
  
      return jsonify({
        'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except actionNotPermittedError:
      abort(401)
    except exceededFeedbackLimitError:
      abort(423) 
    except:
      abort(422)
  
  
  '''
  Endpoint: POST /student_access/request_message
        Description:         This method adds a request message from student to mentor into the database, student_id is decoded from jwt.
                             Mentor_id, course_id, message, needs_volunteer are form inputs from student.        
        Permission:          'post:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/student_access/request_message', methods=['POST'])
  @requires_auth('post:student')
  def student_request_message(student_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
      
      mentor_found = Mentor.query.filter(Mentor.userid==input_request['mentor_id']).one_or_none()
      if mentor_found==None:
        raise resourceNotFoundError  
  
      new_message = RequestMessage( 
                                     mentor_id=input_request['mentor_id'],
                                     student_id=student_id,
                                     course_id=input_request['course_id'],
                                     message=input_request['message'],
                                     needs_volunteer=input_request['needs_volunteer']
                                     )  
      new_message.insert()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  
  '''
  Endpoint: GET /student_access/reply_messages
        Description:         This method returns the reply messages from mentor based on the student id decoded from jwt
        Permission:          'read:student' permission required.
        Return Value:        Returns a list of reply messages as ReplyMessage.format() which contains the message from mentor
        Return data format:  Returns status code 200 and json {"success": True, "reply_messages": list }  
                             or appropriate status code indicating reason for failure
  '''    
  @app.route('/student_access/reply_messages',methods=['GET']) 
  @requires_auth('read:student')
  def student_reply_messages(student_id):
    messages_formatted = []
  
    try:
      messages = ReplyMessage.query.order_by(ReplyMessage.id.desc()).filter(ReplyMessage.student_id==student_id).all()
      if len(messages)!=None:
        messages_formatted = [message.format() for message in messages]
  
      return jsonify({
        'success':True,
        'reply_messages': messages_formatted
        })
  
    except:
      abort(422)
  
  '''
  Endpoint: POST /student_access/admin_message
        Description:         This method adds a request message from student to admin into the database, student_id is decoded from jwt. Message is form input from student.        
        Permission:          'post:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/student_access/admin_message', methods=['POST'])
  @requires_auth('post:student')
  def student_admin_message(student_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
      
      new_message = AdminMessage( 
                                  student_id = student_id,
                                  mentor_id = None,
                                  message=input_request['message']
                                )  
  
      new_message.insert()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except:
      abort(422)
  
  
  ################MENTOR ENDPOINTS#############################

  '''
  Endpoint: POST /mentor_access
        Description:         This method adds a new mentor with new information from user into the database, mentor_id is decoded from jwt
        Permission:          'post:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''  
  @app.route('/mentor_access', methods=['POST'])
  @requires_auth('post:mentor')
  def mentor_new_mentor(mentor_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
  
      mentor = Mentor.query.filter(Mentor.userid==mentor_id).one_or_none()
      if mentor!=None:
        raise alreadyExistsError
  
      new_mentor = Mentor(
                           userid = mentor_id,
                           name = input_request['name'],
                           address = input_request['address'],
                           city = input_request['city'],
                           state = input_request['state'],
                           qualification = input_request['qualification'],
                           add_qualification = input_request['add_qualification'],
                           is_volunteer = input_request['is_volunteer'],
                           price = input_request['price'],
                           avail_time = input_request['avail_time']
                           )
      new_mentor.insert()
  
      return jsonify({
         'success' : True
        })
  
    except alreadyExistsError:
      abort(406)
    except inputNotSpecifiedError:
      abort(400)
    except:
      abort(422)
  
  '''
  Endpoint: GET /mentor_access
        Description:         This method returns the mentor information based on the mentor id decoded from jwt
        Permission:          'read:mentor' permission required.
        Return Value:        Returns Mentor.format() which contains all inforamtion of mentor
                             Courses that the mentor offers which is a list of MentorCourse.format()
                             Previous students that the mentor has tutored as previous_students which is a list of MentorStudentPair.format() which returns student_id, year of tutoring etc                            
                             Current students that the mentor is tutoring as current_students which is a list of MentorStudentPair.format() which returns student id, year of tutoring etc 
                             Feedbacks that the mentor has recived as a list of Feedback.format()
                             Overall rating of the mentor calculated using return_rating method.                            
        Return data format:  Returns status code 200 and json {"success": True, 'mentor_info' : mentor, "courses_offered": list, "previous_students": list, "current_students": list, "feedbacks": list, "rating":int }  
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/mentor_access', methods=['GET'])
  @requires_auth('read:mentor')
  def mentor_mentor_info(mentor_id):
    mentor_formatted = []
    courses_offered_formatted = []
    current_students_formatted = []
    previous_students_formatted = []
    feedbacks_formatted = []
    rating = 0
  
    try:

      mentor = Mentor.query.filter(Mentor.userid==mentor_id).first()
      if mentor!=None:
        mentor_formatted = mentor.format()

      courses_offered = MentorCourse.query.filter(MentorCourse.mentor_id==mentor_id).all()
      if courses_offered!=None:
        courses_offered_formatted = [ course_offered.format() for course_offered in courses_offered ]
  
      current_students = MentorStudentPair.query.filter(MentorStudentPair.mentor_id==mentor_id, MentorStudentPair.present_student==True).all()
      if current_students!=None:
        current_students_formatted = [current_student.format() for current_student in current_students]

      previous_students = MentorStudentPair.query.filter(MentorStudentPair.mentor_id==mentor_id, MentorStudentPair.present_student==False).all()
      if previous_students!=None:
        previous_students_formatted = [previous_student.format() for previous_student in previous_students]
       
      feedbacks = Feedback.query.filter(Feedback.mentor_id==mentor_id).all()
      if feedbacks!=None:
        feedbacks_formatted = [feedback.format() for feedback in feedbacks]

      rating = return_rating(mentor_id)
 
      return jsonify ({
          'success'  : True,
          'mentor_info' : mentor_formatted,
          'current_students' : current_students_formatted,
          'previous_students': previous_students_formatted,
          'courses_offered': courses_offered_formatted,
          'feedbacks': feedbacks_formatted,
          'rating': rating
          })
  
    except:
      abort(422)
  
  '''
  Endpoint: PATCH /mentor_access
        Description:         This method updates existing mentor with new information from user into the database, mentor_id is decoded from jwt
        Permission:          'update:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''  
  @app.route('/mentor_access', methods=['PATCH'])
  @requires_auth('update:mentor')
  def mentor_update_info(mentor_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
  
      update_mentor = Mentor.query.filter(Mentor.userid==mentor_id).one_or_none()
      if update_mentor is None:
        raise resourceNotFoundError
  
      update_mentor.name = input_request['name']
      update_mentor.address = input_request['address']
      update_mentor.city = input_request['city']
      update_mentor.state = input_request['state']
      update_mentor.qualification = input_request['qualification'] 
      update_mentor.add_qualification = input_request['add_qualification']
      update_mentor.is_volunteer = input_request['is_volunteer']
      update_mentor.price = input_request['price']
      update_mentor.avail_time = input_request['avail_time']
  
      update_mentor.update()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  
  '''
  Endpoint: DELETE /mentor_access
        Description:         This method deletes existing mentor from the database, mentor_id is decoded from jwt.
                             Upon deletion of mentor, courses added by mentor and feedbacks to mentor are also deleted.
        Permission:          'delete:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/mentor_access', methods=['DELETE'])
  @requires_auth('delete:mentor')
  def mentor_delete_profile(mentor_id):
    
    try:
      del_mentor = Mentor.query.filter(Mentor.userid==mentor_id).one_or_none()
      if del_mentor==None:
        raise resourceNotFoundError
  
      del_mentor.delete()
   
      return jsonify({
        'success' : True
        })
  
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  
  
  '''
  Endpoint: POST /mentor_access/new_course
        Description:         This method adds a new course with new information from mentor into the database, mentor_id is decoded from jwt
        Permission:          'post:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''  
  @app.route('/mentor_access/new_course', methods=['POST'])
  @requires_auth('post:mentor')
  def mentor_new_course(mentor_id):
  
    try:
      input_request  = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
      
      mentor_found = Mentor.query.filter(Mentor.userid==mentor_id).one_or_none()
      if mentor_found==None:
        raise resourceNotFoundError  

      new_course = MentorCourse(
                               mentor_id = mentor_id,
                               name = input_request['name'],
                               grade = input_request['grade']
                              )
      new_course.insert()
  
      return jsonify({
         'success' : True
      })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  

  '''
  Endpoint: DELETE /mentor_access/delete_course/<course_id>
        Description:         This method deletes existing course from the database, mentor_id is decoded from jwt, course id is expected as input from form.
                             Deletion of course can only be performed by the mentor who added the course. 
        Permission:          'delete:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/mentor_access/delete_course/<course_id>', methods=['DELETE'])
  @requires_auth('delete:mentor')
  def mentor_delete_course(mentor_id,course_id):
  
    try:
      del_mentor_course = MentorCourse.query.filter(MentorCourse.mentor_id==mentor_id,MentorCourse.id==course_id).one_or_none()
      if del_mentor_course==None:
        raise resourceNotFoundError
  
      del_mentor_course.delete()
  
      return jsonify({
        'success' : True
        })
  
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  
  
  
  '''
  Endpoint: GET /mentor_access/students/<student_id>
        Description:         This method returns the student information based on the student id decoded from input request
        Permission:          'read:mentor' permission required.
        Return Value:        Returns Student.format_mentor() which contains all non-confidential information of student
        Return data format:  Returns status code 200 and json {"success": True, "student_details": student }  
                             or appropriate status code indicating reason for failure
  '''  
  @app.route('/mentor_access/students/<student_id>', methods=['GET'])
  @requires_auth('read:mentor')
  def mentor_student_info(mentor_id,student_id):
    student_formatted = []
  
    try:
      student = Student.query.filter(Student.userid==student_id).first()
      if student!=None:
        student_formatted = student.format_mentor()
      else:
        raise resourceNotFoundError
    
      return jsonify({
        'success' : True,
        'student_details': student_formatted
        })
    
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  

  '''
  Endpoint: POST /mentor_access/accept_student
        Description:         This method adds a new entry into MentorStudentPair in the database indicating that the metor has accepted to tutor the student
                             Mentor_id is decoded from jwt. Student_id, course_id, mentorship_year, present_student inputs are recived from input request.
        Permission:          'post:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''     
  @app.route('/mentor_access/accept_student', methods=['POST'])
  @requires_auth('post:mentor')
  def mentor_accept_student(mentor_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError

      student = Student.query.filter(Student.userid==input_request['student_id']).first()
      if student==None:
        raise resourceNotFoundError
      
      new_student = MentorStudentPair( 
                                       mentorship_year= "mentorship_year",
                                       course_id=input_request['course_id'],
                                       mentor_id=mentor_id,
                                       student_id=input_request['student_id'],
                                       present_student = input_request['present_student']
                                       )  
      new_student.insert()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  
  
  '''
  Endpoint: PATCH /mentor_access/accepted_student_update
        Description:         This method updates an existing entry in MentorStudentPair in the database which indicating that the metor has accepted to tutor the student
                             Mentor_id is decoded from jwt. Student_id, course_id, mentorship_year, present_student inputs are recived from input request.
        Permission:          'update:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''    
  @app.route('/mentor_access/accepted_student_update', methods=['PATCH'])
  @requires_auth('update:mentor')
  def mentor_update_student(mentor_id):
    
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
  
      update_student = ( MentorStudentPair.query
                                          .filter(MentorStudentPair.mentor_id==mentor_id,MentorStudentPair.student_id==input_request['student_id'],MentorStudentPair.course_id==input_request['course_id'])
                                          .one_or_none()
                       )
      if update_student is None:
        raise resourceNotFoundError
  
      update_student.present_student=input_request['present_student']
      update_student.mentorship_year=input_request['mentorship_year']
      update_student.course_id=input_request['course_id']
  
      update_student.update()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  
  
  
  '''
  Endpoint: GET /student_access/request_messages
        Description:         This method returns the request messages from students based on the mentor id decoded from jwt
        Permission:          'read:mentor' permission required.
        Return Value:        Returns a list of request messages as RequestMessage.format() which contains the messages from students. It returns in descending order of req message id.
        Return data format:  Returns status code 200 and json {"success": True, "request_messages": list }  
                             or appropriate status code indicating reason for failure
  '''    
  @app.route('/mentor_access/request_messages', methods=['GET'])
  @requires_auth('read:mentor')
  def mentor_request_messages(mentor_id):
    messages_formatted = []
  
    try:
      messages = RequestMessage.query.order_by(RequestMessage.id.desc()).filter(RequestMessage.mentor_id==mentor_id).all()
      if len(messages)!=None:
        messages_formatted = [message.format() for message in messages]
  
      return jsonify({
        'success':True,
        'request_messages': messages_formatted
        })
  
    except:
      abort(422)
  

  '''
  Endpoint: POST /student_access/reply_message
        Description:         This method adds a reply message from mentor to student into the database, mentor_id is decoded from jwt.
                             Student_id, course_id, message, needs_volunteer are form inputs from mentor.        
        Permission:          'post:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/mentor_access/reply_message', methods=['POST'])
  @requires_auth('post:mentor')
  def mentor_reply_message(mentor_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
    
      student = Student.query.filter(Student.userid==input_request['student_id']).first()
      if student==None:
        raise resourceNotFoundError

      new_message = ReplyMessage( 
                                  mentor_id=mentor_id,
                                  student_id=input_request['student_id'],
                                  course_id=input_request['course_id'],
                                  message=input_request['message']
                                )  
  
      new_message.insert()
  
      return jsonify({
         'success' : True
        })
  
    except inputNotSpecifiedError:
      abort(400)
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  
  
  '''
  Endpoint: POST /mentor_access/admin_message
        Description:         This method adds a request message from mentor to admin into the database, mentor_id is decoded from jwt. Message is form input from mentor.        
        Permission:          'post:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/mentor_access/admin_message', methods=['POST']) 
  @requires_auth('post:mentor')
  def mentor_admin_message(mentor_id):
  
    try:
      input_request = request.get_json()
      if input_request is None:
        raise inputNotSpecifiedError
      
      new_message = AdminMessage( 
                                  student_id = None,
                                  mentor_id = mentor_id,
                                  message=input_request['message']
                                )  
      new_message.insert()
    
      return jsonify({
         'success' : True
        })
    
    except inputNotSpecifiedError:
      abort(400)
    except:
      abort(422)
  
  
  ################ADMIN ENDPOINTS###############################

  '''
  Endpoint: GET /admin_access/students
        Description:         This method returns the list of students in the database
        Permission:          'read:admin' permission required.
        Return Value:        Returns list of all students as students.format() which contains all student information
        Return data format:  Returns status code 200 and json {"success": True, "students": list} where students is the list of students
                             or appropriate status code indicating reason for failure
  '''   
  @app.route('/admin_access/students', methods=['GET'])
  @requires_auth('read:admin')
  def f_students(admin_id):
    students_formatted = []
  
    try:
      students = Student.query.all()
      if len(students)!=0:
        students_formatted = [student.format() for student in students]
  
      return jsonify ({
          'success'  : True,
          'students' : students_formatted
          })
  
    except:
      abort(422)
  
  '''
  Endpoint: GET /admin_access/mentors
        Description:         This method returns the list of mentors in the database
        Permission:          'read:admin' permission required.
        Return Value:        Returns list of all mentors as mentor.format() which contains all mentor information
        Return data format:  Returns status code 200 and json {"success": True, "mentors": list} where mentors is the list of mentors
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/admin_access/mentors', methods=['GET'])
  @requires_auth('read:admin')
  def f_mentors(admin_id):
    mentors_formatted = []
  
    try:
      mentors = Mentor.query.all()
      if len(mentors)!=0:
        mentors_formatted = [mentor.format() for mentor in mentors]
  
      return jsonify ({
          'success'  : True,
          'mentors' : mentors_formatted
          })
  
    except:
      abort(422)
  
  '''
  Endpoint: GET /admin_access/view_messages
        Description:         This method returns the admin messages from mentors and students students
        Permission:          'read:admin' permission required.
        Return Value:        Returns a list of admin messages as AdminMessage.format() which contains the messages from students and mentors
        Return data format:  Returns status code 200 and json {"success": True, "request_messages": list }  
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/admin_access/view_messages', methods=['GET'])
  @requires_auth('read:admin')
  def admin_view_messages(admin_id):
    messages_formatted = []
  
    try:
      messages = AdminMessage.query.all()
      if len(messages)!=0:
        messages_formatted = [message.format() for message in messages]
  
      return jsonify ({
          'success'  : True,
          'admin_messages' : messages_formatted
          })
  
    except:
      abort(422)
  
  '''
  Endpoint: DELETE /admin_access/students/<student_id>
        Description:         This method deletes existing student from the database.
        Permission:          'delete:student' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/admin_access/students/<student_id>', methods=['DELETE'])
  @requires_auth('delete:student')
  def admin_student_delete(admin_id,student_id):
  
    try:
      del_student = Student.query.filter(Student.userid==student_id).one_or_none()
      if del_student==None:
        raise resourceNotFoundError
  
      del_student.delete()
  
      return jsonify({
        'success' : True
      })
  
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)
  
  '''
  Endpoint: DELETE /admin_access/mentors/<mentor_id>
        Description:         This method deletes existing mentor from the database.
                             Upon deletion of mentor, courses added by mentor and feedbacks to mentor are also deleted.
        Permission:          'delete:mentor' permission required. 
        Return data format:  Returns status code 200 and json {"success": True}
                             or appropriate status code indicating reason for failure
  ''' 
  @app.route('/admin_access/mentors/<mentor_id>', methods=['DELETE'])
  @requires_auth('delete:mentor')
  def admin_mentor_delete(admin_id,mentor_id):
    
    try:
      del_mentor = Mentor.query.filter(Mentor.userid==mentor_id).one_or_none()
      if del_mentor==None:
        raise resourceNotFoundError
  
      del_mentor.delete()
   
      return jsonify({
        'success' : True
        })
  
    except resourceNotFoundError:
      abort(404)
    except:
      abort(422)  
  
  
  ######################ERROR HANDLING PART2####################################
  
  '''
   Error Handlors for all expected errors
  '''
  
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "unprocessable"
                      }), 422
  
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": "Resource Not Found"
                      }), 404
  
  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
                      "success": False, 
                      "error": 405,
                      "message": "Method Not Allowed"
                      }), 405
  
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": "Bad request, check the input data format"
                      }), 400
  
  @app.errorhandler(406)
  def user_already_exists(error):
      return jsonify({
                      "success": False, 
                      "error": 406,
                      "message": "User already exists, you can update info or delete"
                      }), 406
  
  @app.errorhandler(423)
  def limit_reached_error(error):
      return jsonify({
                      "success": False, 
                      "error": 423,
                      "message": "You can give upto 2 feedbacks per metor, contact admin for more info"
                      }), 423
  
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
                      "success": False, 
                      "error": 500,
                      "message": "Internal Server Error"
                      }), 500
  
  @app.errorhandler(401)
  def unauthorized_error(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message":"not permitted to perform this action"
                  }),401
  
  
  @app.errorhandler(AuthError)
  def auth_error_handler(ex):
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response


  return app


############################################################

APP = create_app()


#############################################################

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
