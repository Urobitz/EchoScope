import requests 

def get_reviews(number_per_page, responses, url,data): #Temporal prototype 
    counter = 0
    for _ in range(responses): 
        print("-----------------------------------------------------------------------------------------------")

        if(counter == params['num_per_page']): #if the counter reaches the upper limit, scroll to next page
            params['cursor'] = data["response"]["cursor"] #Scroll to next page
            r = requests.get(url, params=params) #make the new request
            data = r.json() 
            counter = 0 #Reset counter to again count to upper limit

        print(data['response']['reviews'][counter]['review'])
        counter += 1

url = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/"

params = {
    "appid" : 3241660,
    "num_per_page" : 100, 
    "cursor" : '*'
}

r = requests.get(url, params=params)

data = r.json()

responses = 500 #How many responses we want total

get_reviews(params["num_per_page"], responses, url, data)
