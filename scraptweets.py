import key
import tweepy
import datetime
import pandas as pd
import time


#ini adalah fungsi untuk scrap tweet berdasarkan lat dan long
def scraptweet(name,lat,long):#name adalah place_name
    auth = tweepy.OAuthHandler(
        key.API_KEY,
        key.API_SECRET_KEY
    )
    auth.set_access_token(
        key.ACCESS_TOKEN,
        key.ACCESS_TOKEN_SECRET
    )
    # Create API object
    api = tweepy.API(auth)
    now = datetime.datetime.now()
    
    # Define the parameters for the API call
    q = "" # the search query
    geocode = f"{lat},{long},1km" # latitude, longitude, and radius(radius ganti disini)
    since_id = now - datetime.timedelta(days=8)# start date
    count = 100
    tweets = []

    print("Scrapping Sedang berjalan")

    while True:
        try:
            # Use the cursor to paginate through the results
            tweetmax_at_one_place = 10000
            for tweet in tweepy.Cursor(api.search_tweets, q=q, geocode=geocode, since_id=since_id, count=count,tweet_mode='extended').items(tweetmax_at_one_place):
                text = tweet.full_text.replace("\n", "") # remove newline characters
                date = tweet.created_at
                tweets.append({'text': text, 'geocode': geocode, 'date': date, 'place_name': name})
            break
        except tweepy.errors.TooManyRequests: # type: ignore 
            print("Hit rate limit. Sleeping for 15 minutes.")
            time.sleep(15 * 60) # sleep for 15 minutes
            print("Scrapping Sedang berjalan")
            continue
        except Exception as e:
        # code to handle the exception, for example logging the error or trying to reestablish the connection
            print(f"An error occurred: {e}")
            time.sleep(30)
            print("Scrapping Sedang berjalan")

    pd.DataFrame(tweets).to_csv("tweets.csv",index=False,mode="a",header=False)#ganti nama file output disini
