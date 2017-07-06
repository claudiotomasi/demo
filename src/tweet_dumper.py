#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv, string, random, numpy, codecs, sys
import re,string, random, os, argparse
from utility import utility
#Twitter API credentials
consumer_key = "yrvZ7JAMm8jJ8dsYewLsf7OrA"
consumer_secret = "Xb1Fd6dVykFGScinOfyqiyQKYtBR19ASLSTEaf0Y58vExaaeAC"
access_key = "135605919-s4heOuOWQIszNOIeFdBgh1kESfqlB7Jl471kwqcB"
access_secret = "lH1YZ9VjghCOeCFrS8S4A8oF6Rg9P8pgPrzSG6ipQRjqg"


def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], '')
    char_regex = re.compile('[^a-zA-Z\.\ ]')
    legals  = re.findall(char_regex, text)
    for l in legals:
        text= text.replace(l[0], '')
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,'.')
    words = []
    for word in text.split():
        word = word.strip()
        #TO DO mergiare
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def remove_hashtags_links(tweet):
	return strip_all_entities(strip_links(tweet))

def total_perturbation(string_tweets, pert):
    adjacents_list = utility.adjacents()
    length = len(string_tweets)
    size_perturbation = numpy.uint8(length * 10/ 100)
    lista = list(string_tweets)
    for j in range(1, size_perturbation):
        position = random.randint(1, length-1)
        #while line[what] == ' ' or line[what] == "\'":
        	#what = random.randint(0, length-1)
        key = lista[position]
        set_of_adjacents = adjacents_list[key]
        error = random.choice(set_of_adjacents[1:])
        lista[position] = error
        string_tweets = ''.join(lista)
    pert.write(unicode(string_tweets))


def single_perturbation(f, outtweets):
	for i in outtweets:
		line = i[2].decode('utf-8')
		length = len(line)
		size_perturbation = numpy.uint8(length * 5/ 100)
		for j in range(1, size_perturbation):
			lista = list(line)
			new_char = random.choice(string.letters[:26])
			what = random.randint(1, length-1)
			#while line[what] == ' ' or line[what] == "\'":
				#what = random.randint(0, length-1)
			lista[what] = new_char
			line = ''.join(lista)
		f.write(unicode(line)+" ")


def get_all_tweets(screen_name, language):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    #write the csv
    with open('csv/'+language+'/%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    #divido file per frase splittando per punto
    #ad ogni frase aggiungo punto e spazio
    #creo la lista della frase, controllo che non sia vuota, elimino eventuali spazi all'inizio
    string_tweets = ""
    with codecs.open('originals/'+language+'/%s_original.txt' % screen_name, "w", 'utf-8-sig') as f:
        for tweet in outtweets:
        	line = tweet[2].decode('utf-8')
        	line = remove_hashtags_links(line)
        	string_tweets += line+" "
        f.write(unicode(string_tweets)) #aggiugnere \n ?

    n_tweets = len(outtweets)
    total_characters = 0
    size = (os.stat('originals/'+language+'/%s_original.txt' % screen_name).st_size/100.0)*80
    with codecs.open('originals/'+language+'/%s_original.txt' % screen_name, 'r', 'utf-8-sig') as tweets:
        with codecs.open('training/'+language+'/%s_knowledge_base.txt' % screen_name, 'w', 'utf-8-sig') as know:
            with codecs.open('remain/'+language+'/%s_test_of_remains.txt' % screen_name, 'w', 'utf-8-sig') as test:
                for line in tweets:
                    divisioner_helper(know, line, size, test, total_characters)

    string_tweets = ""
    with codecs.open('remain/'+language+'/%s_test_of_remains.txt' % screen_name, "r", 'utf-8-sig') as f:
    	for tweet in f:
    		string_tweets += tweet


    with codecs.open('test/'+language+'/%s_test_of_remains.txt' % screen_name, "w", 'utf-8-sig') as perturbation:
            total_perturbation(string_tweets, perturbation)

    #with codecs.open("training/%s_singlePert.txt" % screen_name, "w", 'utf-8-sig') as f:
    	#single_perturbation(f, outtweets)


def divisioner_helper(know, line, size, test, total_characters):
    for character in line:
        if total_characters < size:
            total_characters += len(character)
            know.write(unicode(character))
        else:
            test.write(unicode(character))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', help='Select language', choices = ['en', 'it'], default = 'en')
    parser.add_argument('-a', '--account', help='Select language')
    args = parser.parse_args()

    language = args.language
    account = args.account
    #pass in the username of the account you want to download
    get_all_tweets(account, language)
