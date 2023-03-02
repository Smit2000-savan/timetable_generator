# timetable_generator or Timetable Management System 

This is a timetbale generator Web application made with the Django Framework and used django database for database management.
This web application allows timetable coordinator to create the timetable of his wants.
And also We have added a feature for the faculty, that they can give their prefernces for their course's timings.
Based on their preferences coordinator can change the timetable.
We have made slot based timetable which means you need to make a slot of courses and mantain the whole slot compare to individual courses.

•	How to run :

-	Download the project folder in your local PC.

-	Open relevant compiler that can compile the python/django project. eg. Pycharm, VScode.

-	Change the current directory (using “cd” command in terminal) to the 'sri' folder (the folder where manage.py or requirement.txt file is found)

-	Then start virtual environment using following command (in terminal): 
		env\scripts\activate 

-	Then download all the required dependencies listed in 'requirements.txt' via following the command:
		pip install -r requirements.txt	(this command will automatically download all required modules)

-	Then run following command to start the local server:
		python manage.py runserver 

	(if any error occurs to run this command then do migrations first by doing 'python manage.py makemigrations' then 'python manage.py migrate')

-	Then go to the http://127.0.0.1:8000/ site.

•	Project Structure:

-	There are total main folder in project directory named ‘sri’, ‘sriapp’, ‘static’ and ‘templates’ and some files named ‘db.sqlite3’, ‘manage.py’, ‘requirement.txt’.

-	‘sri’ folder : stores all the project settings in ‘settings.py’ and a ‘urls.py’ file to redirect to particular app (here ‘sriapp’).

-	‘sriapp’ : stores all the required files that are used to compile the project. ‘models.py’ stores all the Django models(database tables); ‘views.py’ stores all the Django views that are used to implement the back-end logic of all pages; ‘urls.py’ stores all urls (all the redirections between pages). 

-	‘static’ : stores all the ‘CSS’ files and images that are used in projects.

-	‘templates’ : stores all the HTML files of all pages partitioned in homepage, coordinator and professor.

-	‘db.sqlite3’ : It is a Django built-in database that stores the database.

-	‘requirements.txt’ : stores all the dependencies of our project.

