import requests
import sqlite3
from steam_client import get_reviews


class DatabaseContext:

    def __init__(self, db_connection, db_cursor):
        self._db_connection = db_connection
        self._db_cursor = db_cursor

    # Getters
    def get_db_connection(self):
        return self._db_connection

    def get_db_cursor(self):
        return self._db_cursor


class SteamRequest:

    def __init__(self, appID, review_limit, params):
        self.appID = appID
        self.review_limit = review_limit
        self.params = params

    # Getters
    def get_appID(self):
        return self.appID

    def get_review_limit(self):
        return self.review_limit

    # Get parameter info
    def get_params(self):
        return self.params

    def get_num_per_page(self):
        return self.params["num_per_page"]

    def get_cursor(self):
        return self.params["cursor"]

    def get_day_range(self):
        return self.params["day_range"]

    # Setters
    def set_appID(self, appID):
        self.appID = appID

    def set_review_limit(self, review_limit):
        self.review_limit = review_limit

    # Set parameter info
    def set_params(self, params):
        self.params = params

    def set_num_per_page(self, num_per_page):
        self.params["num_per_page"] = num_per_page

    def set_cursor(self, cursor):
        self.params["cursor"] = cursor

    def set_day_range(self, day_range):
        self.params["day_range"] = day_range


def user_init():
    print("Welcome to EchoScope")
    review_limit = int(input("1.Enter desired amount of reviews: "))
    appID = int(input("2. Enter game appID: "))

    return review_limit, appID


def init_parameters(appID):
    params = {
        "appid": appID,
        "num_per_page": 100,
        "cursor": "*",
        "filter": 1,
        "purchase_type": 1,    # All purchase types
        "languages[0]": "all",  # All languages
        "day_range" : 30
    }

    return params


def init_database():
    db_connection = sqlite3.connect("reviews.db")
    db_cursor = db_connection.cursor()

    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            app_id INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            voted_up INTEGER NOT NULL,
            playtime_at_review INTEGER,
            playtime_forever INTEGER,
            received_for_free INTEGER
        )
        """
    )

    return db_connection, db_cursor


def init():
    url = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/"

    review_limit, appID = user_init()
    params = init_parameters(appID)
    db_connection, db_cursor = init_database()

    instance = SteamRequest(appID, review_limit, params)
    database = DatabaseContext(db_connection, db_cursor)

    get_reviews(url, instance, database)


init()