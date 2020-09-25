## ABOUT THE APP
Mentor-student-web is a platform for students to find part-time/full-time mentors in their city. Mentors can register themselves and add courses that they can teach along with the level at which they would like to teach the course. Students can search mentors using filters such as rating, qualification, street, city, state, tutoring fee, etc. The app also supports a student mentor messaging system through which students can send requests to mentors and mentors can accept potential students. Students can also choose to send feedbacks to the mentors that they are tutoring with. There is also support for an administrative role which can disable reported mentor/student accounts.  

## MOTIVATION FOR THE APP
I thought that it might be a good idea to connect students with part-time mentors or people willing to take some time off to tutor in the area. 

## WEBPAGE  
The webpage is hosted at:  
https://mentor-student-web.herokuapp.com/  

## Instructions to setup authentication
You can find the JWTs for a student, mentor and Admin in `setup.sh`  

Alternatively, you can use the following URL to create a new account:  
https://dev-uda-course.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=Ve7fHhfDb8vqINZ2X16B9ZGeJJuMo5P1&redirect_uri=https://mentor-student-web.herokuapp.com/courses  
Please wait upto 24 hours to get permissions (assign roles) 

The signin page requires a username, email id, password and role:mentor/student/admin

## ENDPOINTS INFO
The following is a brief description of the end points. Please refer to app.py or `setup_instructions/README.md` for detailed description of the endpoints.

### PUBLIC ENDPOINTS
1.  Endpoint: GET /courses  
        Description:         This method returns the list of all unique courses in the database  

### STUDENT ENDPOINTS
Student endpoints are those that a user with role student can access.  

1. POST /student_access  
        Description:         This method adds a new student with new information from user into the database, student_id is decoded from jwt  
2. GET /student_access  
        Description:         This method returns the student information based on the student id decoded from jwt  
3. PATCH /student_access  
        Description:         This method updates existing student with new information from user into the database, student_id is decoded from jwt  
4. DELETE /student_access  
        Description:         This method deletes existing student from the database, student_id is decoded from jwt  
5.  Endpoint: POST /student_access/search_mentors  
        Description:         This method searches for mentors with information from student, student_id is decoded from jwt. The mentor's city and state must match the info given by the student    
                             in the form along with the course name the student inputs and also the grade.  
6.  Endpoint: GET /student_access/mentors/{mentor_id}  
        Description:         This method returns the mentor information based on the mentor id decoded from request  
7.  Endpoint: POST /student_access/feedback  
        Description:         This method adds a feedback from student to mentor into the database, student_id is decoded from jwt. Mentor_id, rating, feedback message are form inputs form Student.  
                             Feedback can only be given by students tutored by mentor. Also, there is a maximum limit of 2 feedbacks per student.   
8.  Endpoint: POST /student_access/request_message  
        Description:         This method adds a request message from student to mentor into the database, student_id is decoded from jwt.  
                             Mentor_id, course_id, message, needs_volunteer are form inputs from student.          
9.  Endpoint: GET /student_access/reply_messages  
        Description:         This method returns the reply messages from mentor based on the student id decoded from jwt   
10. Endpoint: POST /student_access/admin_message  
        Description:         This method adds a request message from student to admin into the database, student_id is decoded from jwt. Message is form input from student.          

### MENTOR END POINTS
1.  Endpoint: POST /mentor_access  
        Description:         This method adds a new mentor with new information from user into the database, mentor_id is decoded from jwt  
2.  Endpoint: GET /mentor_access  
        Description:         This method returns the mentor information based on the mentor id decoded from jwt  
3.  Endpoint: PATCH /mentor_access  
        Description:         This method updates existing mentor with new information from user into the database, mentor_id is decoded from jwt  
4.  Endpoint: DELETE /mentor_access  
        Description:         This method deletes existing mentor from the database, mentor_id is decoded from jwt.  
                             Upon deletion of mentor, courses added by mentor and feedbacks to mentor are also deleted.  
5.  Endpoint: POST /mentor_access/new_course  
        Description:         This method adds a new course with new information from mentor into the database, mentor_id is decoded from jwt  
6.  Endpoint: DELETE /mentor_access/delete_course/{course_id}  
        Description:         This method deletes existing course from the database, mentor_id is decoded from jwt, course id is expected as input from form.  
                             Deletion of course can only be performed by the mentor who added the course.   
7.  Endpoint: GET /mentor_access/students/{student_id}  
        Description:         This method returns the student information based on the student id decoded from input request  
8.  Endpoint: POST /mentor_access/accept_student  
        Description:         This method adds a new entry into MentorStudentPair in the database indicating that the metor has accepted to tutor the student  
                             Mentor_id is decoded from jwt. Student_id, course_id, mentorship_year, present_student inputs are recived from input request.  
9.  Endpoint: PATCH /mentor_access/accepted_student_update  
        Description:         This method updates an existing entry in MentorStudentPair in the database which indicating that the metor has accepted to tutor the student  
                             Mentor_id is decoded from jwt. Student_id, course_id, mentorship_year, present_student inputs are recived from input request.  
10. Endpoint: GET /student_access/request_messages  
        Description:         This method returns the request messages from students based on the mentor id decoded from jwt  
11. Endpoint: POST /student_access/reply_message  
        Description:         This method adds a reply message from mentor to student into the database, mentor_id is decoded from jwt.  
                             Student_id, course_id, message, needs_volunteer are form inputs from mentor.          
12. Endpoint: POST /mentor_access/admin_message  
        Description:         This method adds a request message from mentor to admin into the database, mentor_id is decoded from jwt. Message is form input from mentor.          

### ADMIN ENDPOINTS
1.  Endpoint: GET /admin_access/students  
        Description:         This method returns the list of students in the database  
2.  Endpoint: GET /admin_access/mentors  
        Description:         This method returns the list of mentors in the database  
3.  Endpoint: GET /admin_access/view_messages  
        Description:         This method returns the admin messages from mentors and students students  
4.  Endpoint: DELETE /admin_access/students/{student_id}   
        Description:         This method deletes existing student from the database.  
5.  Endpoint: DELETE /admin_access/mentors/{mentor_id}  
        Description:         This method deletes existing mentor from the database.  
                             Upon deletion of mentor, courses added by mentor and feedbacks to mentor are also deleted.  






<<<<<BEFORE SUBMITTING>>>>>>>>>>
## run tests and make sure things are working
## go to auth0 and set your JWT to maxtiming 
## copy that JWT into setup.sh 
## remove my username and password
## git commit and submit
## IMPORTANT: change my laptop password  
