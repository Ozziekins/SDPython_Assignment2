from sqlalchemy.orm import Session
from src.Task_2 import SqlProvider
from src.Task_2 import Entry
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=SqlProvider.engine)
session = Session()

def statsFor7Days():
#     if today is earlier than 08.10.2022, then print just stats for all the days since start with a note
    summary = [13451, 30, 200001]
    summaryText = f"""Statistics for the past 7 days:
        Total sessions : {summary[0]} 
        Average time spent per session : {summary[1]} min
        Sum of hours spent by all users : {summary[2]} hours"""
    print(summaryText)

    return summaryText

def isSuperUser(userID):
    # a user who has sessions time more than 60 min in a week
    return "Yes"

def queryUserID(userID):
    # num = session.query(Entry.session_id).filter(Entry.client_user_id == userID).count()
    num = session.query(Entry.client_user_id).distinct(Entry.client_user_id).group_by(Entry.client_user_id).count()
    # row = SqlProvider.execute()
    print(num)
    return num

def printUserSummary():
    # 0302549e-5522-43e5-b2f2-0b470932a6fd
    userID = input("Enter user id: \n")

    db = queryUserID(userID)
    print(db)

    # while True:
    #     if userID in db:
    #         # if no interval is given, then give entire summary of this user
    #         # interval = input("Enter period (yyyy/mm/dd - yyyy/mm/dd) : \n")
    #
    #         print(f"""User found!!
    #             User with id : 0116f41a-28b1-4d81-b250-15d7956e2be1
    #                 Number of sessions : 10
    #                 Date of first session : 2021/10/10
    #                 Average time spent per session : 2 hrs
    #                 Date of most recent session : 2022/09/30
    #                 Most frequently used device : Windows
    #                 Devices used : [Mac OS, Windows, Android]
    #                 Average of : 1) Round trip time (RTT) 2) Frames per Second 3) Dropped Frames 4) bitrate
    #                 Total number of bad sessions (predicted using ML model)
    #                 Estimated next session time : 4 hrs
    #                 Super user : Yes\n""")
    #
    #         answer = input("Find another user ? (yes/no) \n")
    #         if answer == "yes":
    #             userID = input("Enter user id: \n")
    #         elif answer == "no":
    #             break
    #         else:
    #             print("Answer not recognized. Exiting\n")
    #             break
    #     else:
    #         print("User cannot be found")
    #         userID = input("Try again, Enter user id: \n")

# def printSessionSummary():
#     # b3aebc80-ff28-4569-bd18-2ace692f668e
#     sessionID = input("Enter session id: \n")

def predictNextSessionDuration():
    pass

def fetchAndUpdateData():
    pass

def topFiveUsers():
    # query our db by time spent and return the 5rows
    pass

def saveToFile(data, file_name):
    with open(file_name+".txt", "w") as f:
        f.write(data)

def exitSession():
    summaryText = statsFor7Days()

    saveSummary = input("Save summary ? (yes/no)\n")
    if saveSummary == "yes":
        saveToFile(summaryText, "summary")
    elif saveSummary == "no":
        pass
    else:
        saveSummary = input("Answer not recognized. Do you want to save the summary? (yes/no) ")

def begin():
    while True:
        choice = int(input("""Choose one operation from below :
            1 : Get status for the past 7 days
            2 : Print user summary 
            3 : Predict user next session duration
            4 : Fetch new data and update users data and ML model
            5 : Get top 5 users based on time spent gaming
            6 : Exit program \n"""))

        if choice == 1:
            statsFor7Days()
        elif choice == 2:
            printUserSummary()
        elif choice == 3:
            predictNextSessionDuration()
        elif choice == 4:
            fetchAndUpdateData()
        elif choice == 5:
            topFiveUsers()
        elif choice == 6:
            exitSession()
            break
        else:
            choice = int(input("Incorrect choice, try again \n"))


if __name__ == "__main__":
    begin()