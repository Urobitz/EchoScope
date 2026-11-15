import requests 
import jsonschema
from jsonschema import validate
import sqlite3


def init_db():
    db = sqlite3.connect("EchoScope.db")
    cursor = db.cursor()


    return db,cursor


def get_reviews(url,params,data,limit,db, cursor): #Temporal prototype 

    current_params = params
    how_many_reviews = 0
    counter = 0

    for _ in range(3): 
        reviews = [block["review"] for block in data["response"]["reviews"]]
        formatted_reviews = [(review,) for review in reviews]
        cursor.executemany('INSERT INTO reviews (review_text) VALUES (?)', formatted_reviews)
        current_params['cursor'] = data['response']['cursor']
        r = requests.get(url, params=current_params)
        data = r.json()

    cursor.execute('SELECT * FROM reviews')
    rows = cursor.fetchall()

    
    print("--- DATABASE CONTENTS ---")
    for row in rows:
        print(row)


    '''#TEST
    reviews = [block["review"] for block in data["response"]["reviews"]]
    print(len(reviews))

    current_params['cursor'] = data['response']['cursor']
    r = requests.get(url, params=current_params)
    data = r.json()

    reviews.append([block["review"] for block in data["response"]["reviews"]])
    print(len(reviews))'''




    '''
for _ in range(int(limit / current_params["num_per_page"])): 




        if(counter == current_params["num_per_page"]): #if the counter reaches the upper limit, scroll to next page
            current_params['cursor'] = data["response"]["cursor"] #Scroll to next page
            r = requests.get(url, params=current_params) #make the new request
            data = r.json() 
            counter = 0 #Reset counter to again count to upper limit
        try:
            print(data['response']['reviews'][counter]['review'])
            how_many_reviews += 1
            
        except IndexError: 
            print("No more reviews to load...")
            return
        counter += 1

    print(f"There were {how_many_reviews} reviews")
'''



def verify_Json(data):
    schema = {
        "type" : "object",
        "properties" : {
            "response" : {
                "type" : "object",
                "properties" : {
                    "reviews" : {
                        "type" : "array",
                        "items" : {
                            "type" : "object",
                            "properties" : {
                                "review": {"type": "string"}
                            },
                            "required" : ["review"]
                        }
                    }
                },
                "required" : ["reviews"]
            }
        },
        "required" : ["response"]
    }

    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        return False

def init(url,params,responses,db,cursor):
    try:
        r = requests.get(url=url, params=params)
        r.raise_for_status()
        data = r.json()
        if not verify_Json(data): 
            raise ValueError("Invalid API response")
        get_reviews(url,params,data,responses,db, cursor)
    except requests.exceptions.RequestException as e: #Raise error if anything happens to the request
        print("EchoScope failed to initialize...")
    


url = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/"
responses = 5000

params = {
    "appid" : 3241660,
    "num_per_page" : 100,
    "day_range" : 365, 
    "cursor" : '*',
    "use_review_quality" : True
}
db, cursor = init_db()
init(url, params,responses,db,cursor)



