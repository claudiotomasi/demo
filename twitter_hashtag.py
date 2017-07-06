import tweepy


consumer_key = "yrvZ7JAMm8jJ8dsYewLsf7OrA"
consumer_secret = "Xb1Fd6dVykFGScinOfyqiyQKYtBR19ASLSTEaf0Y58vExaaeAC"
access_key = "135605919-s4heOuOWQIszNOIeFdBgh1kESfqlB7Jl471kwqcB"
access_secret = "lH1YZ9VjghCOeCFrS8S4A8oF6Rg9P8pgPrzSG6ipQRjqg"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

search_text = "#disney"
search_number = 5
search_result = api.search(search_text, rpp=search_number)
for i in search_result:
    print (i.text)
