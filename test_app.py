import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Student, Mentor, MentorCourse, MentorStudentPair, Feedback, RequestMessage, ReplyMessage, AdminMessage

JWT_STUDENT = os.getenv('JWT_STUDENT')
JWT_MENTOR = os.getenv('JWT_MENTOR')
JWT_ADMIN = os.getenv('JWT_ADMIN')

### Testing will bw done locally.. take your jwt and do this 
class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('anusharavilla:SriSha1234@localhost:5432', self.database_name) # TODO: Change here before testing
        setup_db(self.app, self.database_path, True)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass


    ##PUBLIC END POINTS
    def test_200_courses(self):
        res = self.client().get('/courses')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass

    def test_405_courses(self):
        res = self.client().post('/courses')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],405)
        self.assertEqual(data['message'],'Method Not Allowed')    
        pass

    
    ##STUDENT END POINTS PART 1
    def test01_200_post_student_access(self):
        res = self.client().post(
                                '/student_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "name" : "Apple",
                                           "grade" : 5,
                                           "address" : "Lemon Street",
                                           "city" : "Fremont",
                                           "state" : "CA"
                                        }   
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass 


    def test02_406_post_student_access(self):
        res = self.client().post(
                                '/student_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "name" : "Apple",
                                           "grade" : 5,
                                           "address" : "Lemon Street",
                                           "city" : "Fremont",
                                           "state" : "CA"
                                        }   
                                )
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],406)
        self.assertEqual(data['message'],"User already exists, you can update info or delete")  
        pass


    def test03_200_get_student_access(self):
        res = self.client().get(
                             '/student_access',
                             headers = [
                                         ('Authorization', f'Bearer {JWT_STUDENT}')
                                     ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['student'] is not None
        assert data['current_courses'] is not None
        assert data['previous_courses'] is not None
        pass

    
    def test04_401_get_student_access(self):
        res = self.client().get('/student_access')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass


    def test05_200_patch_student_access(self):
        res = self.client().patch(
                                '/student_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "name" : "Apple patched",
                                           "grade" : 5,
                                           "address" : "Lemon Street",
                                           "city" : "Fremont",
                                           "state" : "CA"
                                        }   
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass 


    def test06_400_patch_student_access(self):
        res = self.client().patch(
                                '/student_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],400)
        self.assertEqual(data['message'],"Bad request, check the input data format")  
        pass


    def test07_200_post_student_access_admin_message(self):
        res = self.client().post(
                                '/student_access/admin_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "message": " student message 1"
                                       }   
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass    

    
    def test08_400_post_student_access_admin_message(self):
        res = self.client().post(
                                '/student_access/admin_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],400)
        self.assertEqual(data['message'],"Bad request, check the input data format")  
        pass
    
    ##### MENTOR ACCESS

    def test09_200_post_mentor_access(self): 
        res = self.client().post(
                                '/mentor_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "name" : "Mentor papaya",
                                          "address" : " Bear Street",
                                          "city" : "Fremont",
                                          "state" : "CA",
                                          "qualification" : "Mentor qualification",
                                          "add_qualification" : "Additional Mentor Qualification",
                                          "is_volunteer" : True,
                                          "price": 40,
                                          "avail_time" : "8:00 am to 9:00 pm, Monday to Thursday"
                                        }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test10_406_post_mentor_access(self):
        res = self.client().post(
                                '/mentor_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "name" : "Mentor somename",
                                          "address" : " Bear Street",
                                          "city" : "Fremont",
                                          "state" : "CA",
                                          "qualification" : "Mentor qualification",
                                          "add_qualification" : "Additional Mentor Qualification",
                                          "is_volunteer" : True,
                                          "price": 40,
                                          "avail_time" : "8:00 am to 9:00 pm, Monday to Thursday"
                                        }
                                )
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],406)
        self.assertEqual(data['message'],"User already exists, you can update info or delete")  
        pass
      
    
    def test11_200_get_mentor_access(self):
        res = self.client().get(
                             '/mentor_access',
                             headers = [
                                         ('Authorization', f'Bearer {JWT_MENTOR}')
                                     ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['mentor_info'] is not None
        assert data['current_students'] is not None
        assert data['previous_students'] is not None
        assert data['courses_offered'] is not None
        assert data['feedbacks'] is not None
        assert data['rating'] is not None
        pass


    def test12_403_get_mentor_access(self):
        res = self.client().get(
                             '/mentor_access',
                             headers = [
                                         ('Authorization', f'Bearer {JWT_STUDENT}')
                                     ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'],"access_denied")
        self.assertEqual(data['description'],"You do not have permission to access this feature")
        pass


    def test13_200_patch_mentor_access(self):
        res = self.client().patch(
                                '/mentor_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "name" : "Mentor papaya",
                                          "address" : "Patch Bear Street",
                                          "city" : "Fremont",
                                          "state" : "CA",
                                          "qualification" : "Mentor qualification",
                                          "add_qualification" : "Additional Mentor Qualification",
                                          "is_volunteer" : True,
                                          "price": 40,
                                          "avail_time" : "8:00 am to 9:00 pm, Monday to Thursday"
                                        }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass    


    def test14_400_patch_mentor_access(self):
        res = self.client().patch(
                                '/mentor_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],400)
        self.assertEqual(data['message'],"Bad request, check the input data format")  

        pass

    
    def test15_200_get_mentor_access_student_info(self):
        res = self.client().get(
                             '/mentor_access/students/student_1',
                             headers = [
                                         ('Authorization', f'Bearer {JWT_MENTOR}')
                                     ]
                                )
        
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)


    def test16_401_get_mentor_access_student_info(self):
        res = self.client().get('/mentor_access/students/student_20')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass    


    
    def test17_200_post_mentor_access_new_course(self): 
        res = self.client().post(
                                '/mentor_access/new_course',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "name": "new_course_1",
                                           "grade": 6
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 

    def test18_405_post_mentor_access_new_course(self):
        res = self.client().get('/mentor_access/new_course')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        pass  
    

    def test19_200_post_mentor_access_accept_student(self): 
        res = self.client().post(
                                '/mentor_access/accept_student',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                         "student_id" : "student_1",
                                         "mentorship_year": "2020",
                                         "present_student" : True,
                                         "course_id" : 1
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test20_400_post_mentor_access_accept_student(self): 
        res = self.client().post(
                                '/mentor_access/accept_student',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')                                           
                                   ],
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'],False)      
        pass 


    def test21_200_patch_mentor_access_accepted_student_update(self): 
        res = self.client().patch(
                                '/mentor_access/accepted_student_update',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                         "student_id" : "student_1",
                                         "mentorship_year": "2019",
                                         "present_student" : False,
                                         "course_id" : 1
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test22_400_patch_mentor_access_accepted_student_update(self): 
        res = self.client().patch(
                                '/mentor_access/accepted_student_update',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')                                           
                                   ],
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'],False)      
        pass 


    def test23_200_get_mentor_access_request_messages(self):
        res = self.client().get(
                             '/mentor_access/request_messages',
                             headers = [
                                         ('Authorization', f'Bearer {JWT_MENTOR}')
                                     ]
                                )        
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['request_messages'] is not None       
        pass

    def test24_401_get_mentor_access_request_messages(self):
        res = self.client().get( '/mentor_access/request_messages')        
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass

    def test25_200_post_mentor_access_reply_message(self): 
        res = self.client().post(
                                '/mentor_access/reply_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                         "student_id": "student_1",
                                         "course_id": 1,
                                         "message": "reply_message"
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test26_400_post_mentor_access_reply_message(self): 
        res = self.client().post(
                                '/mentor_access/reply_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')                                           
                                   ],
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'],False)      
        pass 

    def test27_200_post_mentor_access_admin_message(self): 
        res = self.client().post(
                                '/mentor_access/admin_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                         "message": "Message to admin 1"
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test28_400_post_mentor_access_admin_message(self): 
        res = self.client().post(
                                '/mentor_access/admin_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')                                           
                                   ],
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'],False)      
        pass 



    ##### STUDENT ACCESS PART 2
    def test30_200_post_student_access_search_mentors(self):
        res = self.client().post(
                                '/student_access/search_mentors',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "course_name" : "course",
                                           "grade" : 5,
                                           "city" : "Fremont",
                                           "state" : "CA"
                                        }   
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass 

    

    def test32_400_post_student_access_search_mentors(self):
        res = self.client().post(
                                '/student_access/search_mentors',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],400)
        self.assertEqual(data['message'],"Bad request, check the input data format")  
        pass


    def test33_200_get_student_access_mentors(self):
        res = self.client().get(
                                '/student_access/mentors/arrrrav',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['courses'] is not None
        assert data['mentor_details'] is not None
        pass 

    def test34_404_get_student_access_mentors(self):
        res = self.client().get(
                                '/student_access/mentors/mentor_20',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        pass 


    def test35_200_post_student_access_request_message(self):
        res = self.client().post(
                                '/student_access/request_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "mentor_id": "arrrrav",
                                          "course_id": 1,
                                          "message": "request Message to mentor",
                                          "needs_volunteer": False
                                       } 
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass    


    def test36_401_post_student_access_request_message(self):
        res = self.client().post(
                                '/student_access/request_message',
                                headers = [
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "mentor_id": "arrrrav",
                                          "course_id": 1,
                                          "message": "request Message to mentor",
                                          "needs_volunteer": False
                                       } 
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        pass


    def test37_200_get_student_access_reply_messages(self):
        res = self.client().get(
                                '/student_access/reply_messages',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['reply_messages'] is not None
        pass 

    def test38_401_get_student_access_reply_messages(self):
        res = self.client().get(
                                '/student_access/reply_messages'
                               )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass 
    
   
    def test39_200_post_student_access_feedback(self):
        res = self.client().post(
                                '/student_access/feedback',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "mentor_id": "arrrrav",
                                          "message": "feedback Message 1",
                                          "rating": 4
                                       } 
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass    


    def test40_400_post_student_access_feedback(self):
        res = self.client().post(
                                '/student_access/feedback',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        pass

    def test41_200_post_student_access_admin_message(self): 
        res = self.client().post(
                                '/student_access/admin_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                         "message": "Message to admin 2"
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test42_400_post_student_access_admin_message(self): 
        res = self.client().post(
                                '/student_access/admin_message',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')                                           
                                   ],
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        pass 



    ##### ADMIN ACCESS 
    def test43_200_get_admin_access_mentors(self):
        res = self.client().get(
                                '/admin_access/mentors',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_ADMIN}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['mentors'] is not None
        pass 

    def test44_401_get_admin_access_mentors(self):
        res = self.client().get(
                                '/admin_access/mentors'
                               )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass 
    

    def test45_200_get_admin_access_students(self):
        res = self.client().get(
                                '/admin_access/students',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_ADMIN}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['students'] is not None
        pass 

    def test46_401_get_admin_access_students(self):
        res = self.client().get(
                                '/admin_access/students'
                               )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass 
    
    def test47_200_get_admin_access_view_messages(self):
        res = self.client().get(
                                '/admin_access/view_messages',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_ADMIN}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        assert data['admin_messages'] is not None
        pass 

    def test48_401_get_admin_access_view_messages(self):
        res = self.client().get(
                                '/admin_access/view_messages'
                               )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        pass    


    def test49_200_delete_admin_access_students(self):
        res = self.client().delete(
                                '/admin_access/students/student_1',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_ADMIN}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass


    def test50_405_delete_admin_access_students(self):
        res = self.client().get(
                                '/admin_access/students/student_1',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'],False)
        pass 
    
    def test51_200_delete_admin_access_mentors(self):
        res = self.client().delete(
                                '/admin_access/mentors/arrrrav',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_ADMIN}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass


    def test52_405_delete_admin_access_mentors(self):
        res = self.client().get(
                                '/admin_access/mentors/arrrrav',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'],False)
        pass 

    
    ## ADDING MORE POSTS FOR THE FOLLOWING DELETES 

    def test53_200_post_student_access(self):
        res = self.client().post(
                                '/student_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "name" : "Apple",
                                           "grade" : 5,
                                           "address" : "Lemon Street",
                                           "city" : "Fremont",
                                           "state" : "CA"
                                        }   
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)       
        pass


    def test54_200_post_mentor_access(self): 
        res = self.client().post(
                                '/mentor_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                          "name" : "Mentor papaya",
                                          "address" : " Bear Street",
                                          "city" : "Fremont",
                                          "state" : "CA",
                                          "qualification" : "Mentor qualification",
                                          "add_qualification" : "Additional Mentor Qualification",
                                          "is_volunteer" : True,
                                          "price": 40,
                                          "avail_time" : "8:00 am to 9:00 pm, Monday to Thursday"
                                        }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    def test55_200_post_mentor_access_new_course(self): 
        res = self.client().post(
                                '/mentor_access/new_course',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}'),
                                           ('Content-Type', 'application/json')
                                   ],
                                json = {
                                           "name": "new_course_1",
                                           "grade": 6
                                       }
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)      
        pass 


    ## DELETE mentor and student

    def test94_200_delete_course_mentor_access(self):
        res = self.client().delete(
                                '/mentor_access/delete_course/2',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass


    def test95_401_delete_course_mentor_access(self):
        res = self.client().delete('/mentor_access/delete_course/1')
        self.assertEqual(res.status_code, 401)
        pass 


    def test96_200_delete_student_access(self):
        res = self.client().delete(
                                '/student_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_STUDENT}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass


    def test97_401_delete_student_access(self):
        res = self.client().delete('/student_access')
        self.assertEqual(res.status_code, 401)
        pass   

    
    def test98_200_delete_mentor_access(self):
        res = self.client().delete(
                                '/mentor_access',
                                headers = [
                                           ('Authorization', f'Bearer {JWT_MENTOR}')
                                   ]
                                )
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        pass


    def test99_401_delete_mentor_access(self):
        res = self.client().delete('/mentor_access')
        self.assertEqual(res.status_code, 401)
        pass   

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()