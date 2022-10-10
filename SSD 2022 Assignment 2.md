---
tags: SSD
title: SSD 2022 Assignment 2
---

## Designing systems with python
**Due Date:** 18 October 2022
**Submission Format:** GitHub repository link and presentation with demo. 
**Python version:** Python 3.5 or greater
**Grading:** Each task has 50 points
:::success
This assignments should be done in teams. Each team should have 3 - 5 parcitipants
:::

## Task 1 (50 points)

In this assignment, we will try to exhaust all the characteristics of python and design patterns. The first task is to design and implement a system for classrooms assignment in educational institutions (i.e Innopolis university). The system should be accessed through an interactive terminal.

To implement the system you have to do the following : 

1. Create a class EdInstitution. An institution has a name, set of classrooms and set of lectures auditoriums. 
2. Create two classes whereby their instances are data members for EdInstitution: klassroom and LectureAuditorium. 
3. Both klassroom and LectureAuditorium have data members (capacity, number, variable to indicate if air conditioner is installed or not, activities assigned to the room and their time interval). 
4. Implement a method to print an object using operator overloading. All classes implemented should have a constructor that assigns all the object attributes, get and set methods. 
5. Classrooms and lecture rooms can be assigned to activities for working hours 08:00 – 21:00. 
6. A klassroom and LectureAuditorium object can be assigned to multiple activities but times should not overlap. 
7. For class EdInstitution implement a method to add, remove, saveToFile, restoreFromFile and print all the classrooms in the educational Institution. 
8. The saveToFile method should dump all the object data in .txt file. The restoreFromFile method should restore the object data from a .txt file. (If you are familier with other data storage methods such as json and databases, you are free to use them) 
9. The main program should print the institution summary at exit. 


Example of how the system should work : 

```
$ python mysystem.py 
Choose one operation from below :
    1 : Add classroom or Auditorium to institution
    2 : Print institution summary
    3 : Assign activity to classroom
    4 : Assign activity to LectureAuditorium
    5 : Exit program

1

Enter institution name :
Innopolis university

Enter (classroom - 1 or Auditorium - 2):
2

Enter (capacity, number, air conditioner- yes/no):
100 462 yes

Auditorium succesfully added to Innopolis University

Add another Auditorium to Innopolis University? (yes/no)
no

Choose one one operation from below :
    1 : Add classroom or Auditorium to institution
    2 : Print institution summary
    3 : Assign activity to classroom
    4 : Assign activity to LectureAuditorium
    5 : Exit program
    
5

In database you have :
Innppolis university 
    classrooms : 10 
    Auditorium(s) : 4
    Status for today (now) : 4 available classroom(s) and 1 available classroom(s)
    
    
Kazan Federal University
    classrooms : 10
    Auditorium : 3
    Status for today (now) : 9 available classroom(s) and 1 available classroom(s)

```


## Task 2 (50 points)
The second task is related to machine learning assignment 1. The task is to design and implement a system that will analyze cloud gaming users. Each user has a unique id (`user id`). Every time a user starts playing in the cloud, a `session id` is assigned to that user session. The functionality of the system is as follows: 
1. The system should be able to fetch recent data from an online source
2. Using an interactive terminal it should be possible to search for a user by user id or session by session id
3. The system should be able to print user summary given time period. If time interval the system should display the full summary for the user since first session.
4. User summary should at least contain the following : 
    * Number of sessions
    * Date of first session
    * Date of most recent session
    * Average time spent per session
    * Most frequently used device
    * Devices used
    * Average of : 1) Round trip time (RTT) 2) Frames per Second 3) Dropped Frames 4) bitrate 
    * Total number of bad sessions (predicted using ML model)
    * Estimated next session time
    * Super user or Not (a user who has sessions time more than 60 min in a week)
5. The system should give an option to save summary to `.txt` file
6. Upon exit the system should display the summary for the past 7 days (number of sessions for all sessions, average time spent per session, sum of hours spent by all users) and option to save it to file  
<!--6. The system should be able to automatically retrain the machine learning model every 3 days and when new data is available. Note that the model should be **updated only** if the new model performs better than the previous model.-->


To estimate the next session time the system should use a machine learning model of your choice or simple mean value of previous sessions spent time. Remember that its better to train your model with data without anomalies. To predict the stream quality, the input of the model should be at least the average and standard deviation of the session raw data as in the machine learning assignment. To get a single session for a user you will first have to group the data by user id then by session id. 

Example of how the is expected to work : 

```
$ python gaming_users_system.py 
Choose one operation from below :
    1 : Get status for the past 7 days
    2 : Print user summary 
    3 : Predict user next session duration
    4 : Fetch new data and update users data and ML model
    5 : Get top 5 users based on time spent gaming
    6 : Exit program
    
2

Enter user id:
0116f41a-28b1-4d81-b250-15d7956e2be1

Enter period (yy/mm/dd - yy/mm/dd) :
2022/07/10 - 2022/08/10

User found!! 
User with id : 0116f41a-28b1-4d81-b250-15d7956e2be1
    Number of sessions : 10
    Date of first session : 2021/10/10
    Average time spent per session : 2 hrs
    Date of most recent session : 2022/09/30
    Most frequently used device : Windows
    Devices used : [Mac OS, Windows, Android]
    Estimated next session time : 4 hrs
    Super user : Yes

Find another user ? (yes/No)
No

Choose one operation from below :
    1 : Get status for the past 7 days
    2 : Print user summary 
    3 : Predict user next session duration
    4 : Fetch new data and update users data and ML model
    5 : Get top 5 users based on time spent gaming
    6 : Exit program
    
6

Statistics for the past 7 days:
    Total sessions : 13451 
    Average time spent per session : 30 min
    Sum of hours spent by all users : 200001 hours
    
Save summary ? (yes/no)
no

Good bye!!
```

The data is stored in **[google drive](https://drive.google.com/drive/folders/1nfrYxDm7TLzls9pedZbLX5rP4McVDWDe?usp=sharing)**. To simulate real world scenario, 5 minutes in your system should be equivalent to one day. All the data should not me downloaded all at once. The format of the data files : raw_{year}\_{month}\_{day}.csv. 

:::danger
For the final presentation, one team member will be chosen randomly to present the project and show demo and the person to answer questions  will be chosen randomly. Failure to answer question has an impact to every member of the team. At least one design pattern should be used in your system and the choice should be justified. 
:::

## Bonus (10 points)
Create a Docker container for running one of the systems from above.




