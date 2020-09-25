# SETUP DEV AND HEROKU DEPLOYMENT

## DEVELOPMENT SET UP INSTRUCTIONS

### PYTHON UPDATE
pip install --upgrade pip

### VIRTUAL ENV
python3 -m venv <env_name>  
source env_name/bin/activate

### REQUIREMENTS
pip install -r requirements.txt

### DATABASE 
Change the DATABASE_URL in setup.sh to reflect local database url and run:  
source setup.sh

### MIGRATIONS FOR DATABASE SCHEMA UPDATE
python manage.py db init  
python manage.py db migrate  
python manage.py db upgrade  

### RUNNING THE SERVER
export FLASK_APP=flaskr  
export FLASK_ENV=development  
flask run --reload

## TEST SETUP
Edit TEST_DB_PATH and TEST_DB_NAME in test_script.sh and run it to test locally:   
source test_script.sh

## DEPLOY TO HEROKU 
1. Create an account in heroku:   
    www.heroku.com  
2. Install Heroku by running:   
    brew tap heroku/brew && brew install heroku  
3. Use this command and login to heroku from terminal  
    heroku login  
4. Create heroku app  
    heroku create name_of_your_app  
5. Add git remote for heroku to local repository  
    git remote add heroku heroku_git_url  
6. Postgres add on for database  
    heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application  
7. To check config variables:  
    heroku config --app name_of_your_application  
    Add your config variables in the REVEAL CONFIG VARS section of setting on the heroku website  
8. To deploy run:  
    git push heroku master  
9. Run migrations using:  
    heroku run python manage.py db upgrade --app name_of_your_application 



## ENDPOINTS IN DETAIL

### PUBLIC ENDPOINTS
1.  Endpoint: GET /courses  
        Description:         This method returns the list of all unique courses in the database  
        Permission:          no permission required.  
        Return Value:        Returns only the name and the grade for each course  
        Return data format:  Returns status code 200 and json {"success": True, "courses": courses} where courses is the list of courses   
                             or appropriate status code indicating reason for failure  
  
### STUDENT ENDPOINTS
1.  Endpoint: POST /student_access  
        Description:         This method adds a new student with new information from user into the database, student_id is decoded from jwt  
        Permission:          'post:student' permission required.  
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
2.  Endpoint: GET /courses  
        Description:         This method returns the list of all unique courses in the database  
        Permission:          no permission required.  
        Return Value:        Returns only the name and the grade for each course  
        Return data format:  Returns status code 200 and json {"success": True, "courses": courses} where courses is the list of courses  
                             or appropriate status code indicating reason for failure   	
3.  Endpoint: PATCH /student_access  
        Description:         This method updates existing student with new information from user into the database, student_id is decoded from jwt  
        Permission:          'update:student' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
4.  Endpoint: DELETE /student_access  
        Description:         This method deletes existing student from the database, student_id is decoded from jwt  
        Permission:          'delete:student' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
5.  Endpoint: POST /student_access/search_mentors  
        Description:         This method searches for mentors with information from student, student_id is decoded from jwt. The mentor's city and state must match the info given by the student    
                             in the form along with the course name the student inputs and also the grade.  
        Permission:          'read:student' permission required.   
        Return Value:        The search output will include a list of mentors with the following mentor information: the mentor_id, time_available, grade, course name, course id.  
        Return data format:  Returns status code 200 and json {"success": True, "search_output":search_output}  
                             or appropriate status code indicating reason for failure  
6.  Endpoint: GET /student_access/mentors/{mentor_id}  
        Description:         This method returns the mentor information based on the mentor id decoded from request  
        Permission:          'read:student' permission required.  
        Return Value:        Returns Mentor.format_student() which contains all non-confidential information of mentor  
                             Courses that the mentor offers which is a list of MentorCourse.format()  
        Return data format:  Returns status code 200 and json {"success": True, "mentor_details": mentor, "courses": list }    
                             or appropriate status code indicating reason for failure  
7.  Endpoint: POST /student_access/feedback  
        Description:         This method adds a feedback from student to mentor into the database, student_id is decoded from jwt. Mentor_id, rating, feedback message are form inputs form Student.  
                             Feedback can only be given by students tutored by mentor. Also, there is a maximum limit of 2 feedbacks per student.   
        Permission:          'post:student' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
8.  Endpoint: POST /student_access/request_message  
        Description:         This method adds a request message from student to mentor into the database, student_id is decoded from jwt.  
                             Mentor_id, course_id, message, needs_volunteer are form inputs from student.          
        Permission:          'post:student' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
9.  Endpoint: GET /student_access/reply_messages  
        Description:         This method returns the reply messages from mentor based on the student id decoded from jwt   
        Permission:          'read:student' permission required.   
        Return Value:        Returns a list of reply messages as ReplyMessage.format() which contains the message from mentor  
        Return data format:  Returns status code 200 and json {"success": True, "reply_messages": list }    
                             or appropriate status code indicating reason for failure  
10. Endpoint: POST /student_access/admin_message  
        Description:         This method adds a request message from student to admin into the database, student_id is decoded from jwt. Message is form input from student.          
        Permission:          'post:student' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  

### MENTOR END POINTS
1.  Endpoint: POST /mentor_access  
        Description:         This method adds a new mentor with new information from user into the database, mentor_id is decoded from jwt  
        Permission:          'post:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
2.  Endpoint: GET /mentor_access  
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
3.  Endpoint: PATCH /mentor_access  
        Description:         This method updates existing mentor with new information from user into the database, mentor_id is decoded from jwt  
        Permission:          'update:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
4.  Endpoint: DELETE /mentor_access  
        Description:         This method deletes existing mentor from the database, mentor_id is decoded from jwt.  
                             Upon deletion of mentor, courses added by mentor and feedbacks to mentor are also deleted.  
        Permission:          'delete:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
5.  Endpoint: POST /mentor_access/new_course  
        Description:         This method adds a new course with new information from mentor into the database, mentor_id is decoded from jwt  
        Permission:          'post:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
6.  Endpoint: DELETE /mentor_access/delete_course/{course_id}  
        Description:         This method deletes existing course from the database, mentor_id is decoded from jwt, course id is expected as input from form.  
                             Deletion of course can only be performed by the mentor who added the course.   
        Permission:          'delete:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
7.  Endpoint: GET /mentor_access/students/{student_id}  
        Description:         This method returns the student information based on the student id decoded from input request  
        Permission:          'read:mentor' permission required.  
        Return Value:        Returns Student.format_mentor() which contains all non-confidential information of student  
        Return data format:  Returns status code 200 and json {"success": True, "student_details": student }    
                             or appropriate status code indicating reason for failure  
8.  Endpoint: POST /mentor_access/accept_student  
        Description:         This method adds a new entry into MentorStudentPair in the database indicating that the metor has accepted to tutor the student  
                             Mentor_id is decoded from jwt. Student_id, course_id, mentorship_year, present_student inputs are recived from input request.  
        Permission:          'post:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
9.  Endpoint: PATCH /mentor_access/accepted_student_update  
        Description:         This method updates an existing entry in MentorStudentPair in the database which indicating that the metor has accepted to tutor the student  
                             Mentor_id is decoded from jwt. Student_id, course_id, mentorship_year, present_student inputs are recived from input request.  
        Permission:          'update:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
10. Endpoint: GET /student_access/request_messages  
        Description:         This method returns the request messages from students based on the mentor id decoded from jwt  
        Permission:          'read:mentor' permission required.  
        Return Value:        Returns a list of request messages as RequestMessage.format() which contains the messages from students. It returns in descending order of req message id.  
        Return data format:  Returns status code 200 and json {"success": True, "request_messages": list }    
                             or appropriate status code indicating reason for failure  
11. Endpoint: POST /student_access/reply_message  
        Description:         This method adds a reply message from mentor to student into the database, mentor_id is decoded from jwt.  
                             Student_id, course_id, message, needs_volunteer are form inputs from mentor.          
        Permission:          'post:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
12. Endpoint: POST /mentor_access/admin_message  
        Description:         This method adds a request message from mentor to admin into the database, mentor_id is decoded from jwt. Message is form input from mentor.          
        Permission:          'post:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  

### ADMIN ENDPOINTS
1.  Endpoint: GET /admin_access/students  
        Description:         This method returns the list of students in the database  
        Permission:          'read:admin' permission required.  
        Return Value:        Returns list of all students as students.format() which contains all student information  
        Return data format:  Returns status code 200 and json {"success": True, "students": list} where students is the list of students  
                             or appropriate status code indicating reason for failure  
2.  Endpoint: GET /admin_access/mentors  
        Description:         This method returns the list of mentors in the database  
        Permission:          'read:admin' permission required.  
        Return Value:        Returns list of all mentors as mentor.format() which contains all mentor information  
        Return data format:  Returns status code 200 and json {"success": True, "mentors": list} where mentors is the list of mentors  
                             or appropriate status code indicating reason for failure  
3.  Endpoint: GET /admin_access/view_messages  
        Description:         This method returns the admin messages from mentors and students students  
        Permission:          'read:admin' permission required.  
        Return Value:        Returns a list of admin messages as AdminMessage.format() which contains the messages from students and mentors  
        Return data format:  Returns status code 200 and json {"success": True, "request_messages": list }    
                             or appropriate status code indicating reason for failure  
4.  Endpoint: DELETE /admin_access/students/{student_id}   
        Description:         This method deletes existing student from the database.  
        Permission:          'delete:student' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  
5.  Endpoint: DELETE /admin_access/mentors/{mentor_id}  
        Description:         This method deletes existing mentor from the database.  
                             Upon deletion of mentor, courses added by mentor and feedbacks to mentor are also deleted.  
        Permission:          'delete:mentor' permission required.   
        Return data format:  Returns status code 200 and json {"success": True}  
                             or appropriate status code indicating reason for failure  

