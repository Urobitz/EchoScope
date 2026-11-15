import requests
import math
from math import ceil
def fetch_website(url, params):
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        response = r.json()
        return response
    except requests.exceptions.RequestException as e:
        print("Failed to fetch website due to the following error: \n e")

def get_reviews(url, params, db_cursor, review_limit, appID, db_connection): #Temporal prototype 

    
    reviews_per_page = params["num_per_page"]
    next_page_cursor = ''
    

    for _ in range(math.ceil((review_limit) / reviews_per_page)):
        reviews_data = fetch_website(url, params)

        next_page_cursor = reviews_data["response"]["cursor"]

        reviews = [
            (
                review["recommendationid"],
                appID,
                review["review"],
                review["voted_up"],
                review["author"]["playtime_at_review"],
                review["author"]["playtime_forever"],
                review["received_for_free"],
            )
            for review in reviews_data["response"]["reviews"]
        ]

        db_cursor.executemany(
                    """INSERT INTO reviews (
                        review_id,
                        app_id,
                        review_text,
                        voted_up,
                        playtime_at_review,
                        playtime_forever,
                        received_for_free)
                        values (?,?,?,?,?,?, ?) ON CONFLICT DO NOTHING""", reviews)

        params["cursor"] = next_page_cursor

    db_connection.commit()



























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