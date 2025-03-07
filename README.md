# CSE111-Python-Final-Project
This is the final project for my CSE111 - Programming with functions module from BYU Idaho

Second Report for a Student Chosen Project

### 1. Time Log Table

I am already a software engineer working with PHP and Python, and this background helps me intuitively with my school work.
Below is a detailed log of the time spent working on my project. 

            Time Spent
   Date       (hours)   Description of Work
----------  ----------  -------------------------
2025-02-15      8      Started my Saturday at 6 am and was only done around 3 pm 
                       - Revisited my Full Stack Web Development Bootcamp material to remind myself about RapidAPI (OpenWeather) documentation 
                         and further went into My Software Engineering Bootcamp materials for data strctures and file handling - HyperionDev and Optimi College
                       - BYU course materials: file handling and data structures and https://www.w3schools.com/python/python_file_handling.asp
                       - tkinter  Source: https://docs.python.org/3/library/tkinter.html, https://realpython.com/python-gui-tkinter/, FreeCode Camp Tkinkter GUI - https://www.youtube.com/watch?v=YXPyB4XeYLA
                       - messagebox and filedialog Source: https://docs.python.org/3/library/tkinter.html, https://www.tutorialspoint.com/python/python_gui_programming.htm
                       - requests  Source: https://docs.python-requests.org, https://www.w3schools.com/python/module_requests.asp, https://www.geeksforgeeks.org/python-requests-tutorial/
                       - pandas  Source: https://pandas.pydata.org, https://www.w3schools.com/python/pandas/default.asp
                       - json_normalize Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html
                       - mysql.connector  Source: https://dev.mysql.com/doc/connector-python/en/
                       - matplotlib.pyplot Source: https://matplotlib.org/stable/api/pyplot_api.html, https://www.w3schools.com/python/matplotlib_intro.asp
                       - os  Source: https://docs.python.org/3/library/os.html
                       - shutil Source: https://docs.python.org/3/library/shutil.html
                       - glob Source: https://docs.python.org/3/library/glob.html

I seperated the development into three parts , like the waterfall style of the software development life cycle : 

2025-02-16      3      1. Skeleton code or basic functionality which was to get the program to call the API, store the data in DB and CSV and output the results to the user 
                       and debugged the errors and error handling for this phase. I decided to use hint type notation for my functions because it makes it easier to understand what data type is expected in the function for the reader


2025-02-16      4      2. Added the second layer of logic which was to visualize the data which has been stored in the DB and used data frame and matpolib plot to create the charts. 
                       This took a lot of trial and error and a lot of re-reading nad mathematical thinking but it was worth it.


2025-02-16      2      3. I Added the last layer which is the OS and Shutil module in order to rename and organize the files but because this manipulates the users OS, 
                       I decided the user should decide if they want to use it or not as opposed to automating it. 


2025-02-17      2.0    Wrote the tests of the program and recorded video to show how the program works.

2025-02-19      3      - Tests were not working had so writing for each piece of logic. 
                       - Just finished the API test quota for the month but luckily after testing the store_data_in_mysql() function.
                         So my marker will need a new free key via https://rapidapi.com/worldapi/api/open-weather13/playground/apiendpoint_d15cd885-e8e5-49e7-b94b-588c41687aa1  
                         
                       - I see that because my quota is finished I am unable to shoot a video.
                         To test :
                        1. kindly install XAMPP AND MySQL Workbench 
                        2. Next to MySQL, click on config and go to the row which says "password = YOUR_PASSWORD" and delete the "YOUR_PASSWORD" and leave it blank and save
                        3. Open Workbench and create a connect with user "root" and a blank password and save the connection
                        4. Open the connection and create a new schema called "test"
                        5. The program already has the SQL Command to create the table so everything should work
                        6. I have attached images to assist with the setup.

                        If any more information is needed please contact me at lngombane@byupathway.edu
```

