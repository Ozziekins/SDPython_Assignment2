from sqlalchemy.orm import Session
from src import SqlProvider
from src import Entry
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

sqlProvider = SqlProvider()

Session = sessionmaker(bind=sqlProvider.engine)
session = Session()

def statsFor7Days():
    # if today is earlier than start day - 7days, then print just stats for all the days since start with a note
    df = pd.read_sql_query('select * from "Entries";', con=sqlProvider.engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    total_sessions = df.session_id.nunique()

    sessions_time = df.groupby(["client_user_id", "session_id"])["timestamp"].agg(["max", "min"])
    sessions_time["diff"] = sessions_time["max"] - sessions_time["min"]
    average_time_per_session = round(sessions_time["diff"].mean() / pd.Timedelta('1 minute'), 2)

    sum_of_hours = round(sessions_time["diff"].sum() / pd.Timedelta('1 hour'), 2)

    summaryText = f"""Statistics for the past 7 days:
        Total sessions : {total_sessions} 
        Average time spent per session : {average_time_per_session} min
        Sum of hours spent by all users : {sum_of_hours} hours \n"""
    print(summaryText)

    return summaryText

def isSuperUser(userID, df):
    # a user who has sessions time more than 60 min in a week
    sessions_time = df.groupby("session_id")["timestamp"].agg(["max", "min"])
    sessions_time["diff"] = sessions_time["max"] - sessions_time["min"]
    total_session = sessions_time["diff"].sum() / pd.Timedelta('1 minute')

    if total_session > 60:
        return "Yes"
    else:
        return "No"

def printUserSummary():
    # 07393db8-e059-4cbd-b16f-88ab2019f045
    userID = input("Enter user id: \n")

    df = pd.read_sql_query('select * from "Entries";', con=sqlProvider.engine)

    while True:
        if userID in set(df['client_user_id']):
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            df.query(f"client_user_id == '{userID}'", inplace=True)
            num_sessions = df.session_id.nunique()

            df.sort_values(by="timestamp")
            df["just_date"] = df["timestamp"].dt.date
            first_session = df["just_date"].iat[0]

            sessions_time = df.groupby("session_id")["timestamp"].agg(["max", "min"])
            sessions_time["diff"] = sessions_time["max"] - sessions_time["min"]
            average_per_session = sessions_time["diff"].mean() / pd.Timedelta('1 minute')

            df.sort_values(by="timestamp", ascending=False)
            recent_session = df["just_date"].iat[0]

            most_device = df["device"].mode().values

            devices = df["device"].unique()

            super_user = isSuperUser(userID, df)

            rtt = round(df["RTT"].mean(), 3)
            fps = round(df["FPS"].mean(), 3)
            dropped_frames = round(df["dropped_frames"].mean(), 3)
            bitrate = round(df["bitrate"].mean(), 3)

            # if no interval is given, then give entire summary of this user
            # interval = input("Enter period (yyyy/mm/dd - yyyy/mm/dd) : \n")

            print(f"""User found!!
                User with id : {userID}
                    Number of sessions : {num_sessions}
                    Date of first session : {first_session}
                    Average time spent per session : {average_per_session} minutes
                    Date of most recent session : {recent_session}
                    Most frequently used device : {most_device}
                    Devices used : {devices}
                    Average of : 1) Round trip time is {rtt} (RTT) 2) Frames per Second is {fps} 3) Dropped Frames is {dropped_frames} 4) bitrate is {bitrate}
                    Total number of bad sessions (predicted using ML model)
                    Estimated next session time : 4 hrs
                    Super user : {super_user}\n""")

            answer = input("Find another user ? (yes/no) \n")
            if answer == "yes":
                userID = input("Enter user id: \n")
                df = pd.read_sql_query('select * from "Entries";', con=sqlProvider.engine)
            elif answer == "no":
                break
            else:
                print("Answer not recognized. Exiting\n")
                break
        else:
            print("User cannot be found")
            userID = input("Try again, Enter user id: \n")

# def printSessionSummary():
#     # b3aebc80-ff28-4569-bd18-2ace692f668e
#     sessionID = input("Enter session id: \n")

def predictNextSessionDuration():
    pass

def fetchAndUpdateData():
    pass

def topFiveUsers():
    # query our db by time spent and return the 5rows
    df = pd.read_sql_query('select * from "Entries";', con=sqlProvider.engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    sessions_time = df.groupby(["client_user_id", "session_id"])["timestamp"].agg(["max", "min"])
    sessions_time["diff"] = sessions_time["max"] - sessions_time["min"]
    sessions_time_total = sessions_time.groupby("client_user_id")["diff"].agg(["sum"])
    sessions_time_total["hours spent gaming"] = sessions_time_total["sum"].dt.components["hours"]
    sessions_time_total = sessions_time_total.sort_values(by="sum", ascending=False)

    top_users = sessions_time_total.head(5)
    print("Top users are: \n", top_users, "\n")


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