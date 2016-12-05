'''
Twitter_Presidential_Race_Sentiment_Clustering: PullTwitterData.py
Authors: Justin Murphey, Rafael Zamora
Last Updated: 12/04/16

CHANGE-LOG:
-Code Review/Refactoring
-Updated Comments

'''

"""
This script is used to pull historic data from Twitter.
It uses a modified version of got3 by Jefferson-Henrique.
CSV files of Tweet data produced per day are generated.

For this analysis, we are interested in the text of the tweet object.
The following attributes are pulled from each tweet:
-author_id :str
-date :str
-text :str

"""

import sys, os, datetime
import GetOldTweets_Python3 as got3
from multiprocessing import Pool

path_to_data = "/Twitter_Presidential_Race_Sentiment_Clustering/data/"
filename_ = "Twitter_Trump_Clinton"

def pull_tweets(args_list):
    '''
    pull_tweets() uses 'args' to run got3 tweet pull and saves the tweet data
    to a CSV file. 'args': [date_obj, keywords, lang, pull_size]

    '''
    for args in args_list:
        date_obj, keywords, lang, pull_size = args
        start_date =  date_obj.strftime("%Y-%m-%d")
        end_date = (date_obj + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        filename = filename_ + "_" + start_date + ".csv"

        print("Pulling Twitter Data from: " + start_date)
        tweetCriteria = got3.manager.TweetCriteria().setLang(lang).setQuerySearch(keywords).setSince(start_date).setUntil(end_date).setMaxTweets(pull_size)
        results = got3.manager.TweetManager.getTweets(tweetCriteria)
        os.makedirs(os.path.dirname(path_to_data+"raw/"+filename), exist_ok=True)
        with open(path_to_data+"raw/"+filename, "w") as f:
            for tweet in results:
                tweet_text = tweet.text
                tweet_date = str(tweet.date)
                tweet_usr_id = str(tweet.author_id)
                f.write(tweet_usr_id + "," + tweet_date + "," + tweet_text + "\n")
        print("\nTweets: " , len(results), "\nFirst Tweet Date: ", results[0].date, "\nLast Tweet Date: ", results[-1].date)

if __name__ == '__main__':
    '''
    Parameters:
    parallel -set True to run distributed pull requests
    cores -number of cores used for distributed pull
    lang -lanuage of tweets
    sample_size -max size of pull for each day, if 0 returns all

    '''
    parallel = False;
    cores = 2;
    lang = "en"
    pull_size = 0
    keywords = "@hillaryclinton OR #hillaryclinton OR Hillary Clinton OR Hillary OR @RealDonaldTrump OR #donaldtrump OR Donald Trump OR Trump"
    start_date = "2016-10-16"
    days = 30

    '''
    Create arguments list for all pulls.

    '''
    args_list = []
    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(days):
        day_date_obj = start_date_obj + datetime.timedelta(days=i)
        args = [day_date_obj, keywords, lang, pull_size]
        args_list.append(args)

    #Used for debugging
    #removeset = set([0])
    #args_list = [v for i, v in enumerate(args_list) if i not in removeset]

    '''
    Run pulls using arguments list.

    '''
    if parallel:
        args_list_parts = [args_list[i::cores] for i in range(cores)]
        with Pool() as pool:
            pool.map(pull_tweets, args_list_parts)
    else: pull_tweets(args_list)
