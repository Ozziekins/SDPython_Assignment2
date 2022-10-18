# Software Design with Python Assignment2
Assignment 2 for the course [F22] Software Design with Python

## Task 1: CLI system for Educational Institutions

The system that allows to manage the existing universities. It allows adding the rooms, auditoriums and assigning activities to them. Summaries for the Universities are represented in a human-readable form.

### How to run

1. In order to run the task, clone the repository. Then navigate from command line to the Task1 folder.
2. `pip install -r requirements.txt`
3. `python main.py`

### How to run with Docker

To run with Docker, just type those 2 commands:

```
docker pull pain122/task1:1.0.0
docker run -ti pain122/task1:1.0.0
```

---
## Task 2: Gaming Users System

The system fetches data from an online store and analyzes it to make predictions on the stream quality and session duration. It also provides statistical summary via an interactive terminal.  

### How to run

1. first, git clone `git clone git@github.com:Ozziekins/SDPython_Assignment2.git`  
2. `cd Task2/`  
3. run `docker-compose up`  
4. open another terminal and run `python3 /src/__main.py__`
5. finally, play around the terminal :)
