import requests 
import sqlite3
from steam_client import get_reviews

def user_init():

    print("Welcome to EchoScope")
    review_limit = int(input("1.Enter desired amount of reviews: "))
    appID = input("2. Enter game appID: ")

    return review_limit, appID

def init_parameters(appID): 

    params = {
        "num_per_page" : 100, #Assume maximum for now
        "appID" : appID,
        "cursor" : "*", #Start at first page
        "day_range" : 365
    }

    return params

def init_database():
    db_connection = sqlite3.connect("reviews.db") 
    db_cursor = db_connection.cursor()

    db_cursor.execute(""" 
        CREATE TABLE IF NOT EXISTs reviews(
            review_id TEXT PRIMARY KEY,
            app_id INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            voted_up INTEGER NOT NULL,
            playtime_at_review INTEGER,
            playtime_forever INTEGER,
            received_for_free INTEGER)""")

    return db_connection,db_cursor

def init():

    url = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/"
    review_limit, appID = user_init()
    params = init_parameters(appID)
    db_connection, db_cursor = init_database()


    get_reviews(url, params, db_cursor, review_limit,appID, db_connection)
    
init()





