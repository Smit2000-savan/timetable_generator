# timetable_generator

This is a timetbale generator Web application made with the Django Framework and used django database for database management.
This web application allows timetable coordinator to create the timetable of his wants.
And also We have added a feature for the faculty, that they can give their prefernces for their course's timings.
Based on their preferences coordinator can change the timetable.
We have made slot based timetable which means you need to make a slot of courses and mantain the whole slot compare to individual courses.

How to run this project:

1. cd to the 'sri' folder (the folder where manage.py is found)
2. Start virtual environment : 
	  env\scripts\activate 
3. Download all the required depedecies listed in 'requirements.txt' via following the command:
	  pip install -r requirements.txt	(this command will automatically download all required modules)
4. Run following command:
	  python manage.py runserver 
	  (if any error occur to run this command then do migrations first by doing 'python manage.py makemigrations' then 'python manage.py migrate')
