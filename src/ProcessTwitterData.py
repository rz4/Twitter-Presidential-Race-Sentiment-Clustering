'''
Twitter_Presidential_Race_Sentiment_Clustering: ProcessTwitterData.py
Authors: Justin Murphey, Rafael Zamora
Last Updated: 12/04/16

CHANGE-LOG:
-Code Review/Refactoring
-Updated Comments

'''

"""
This script is used to process data gathered from Twitter
and generate a data set which will be used in the cluster analysis.

"""

import os, json, re
import numpy as np
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from difflib import SequenceMatcher
from multiprocessing import Pool

path_to_data = "/Twitter_Presidential_Race_Sentiment_Clustering/data/"

def process_tweet_data(tweets_data):
    '''
    process_tweet_data() calculates the candidate reference value and sentiment
    value of tweet data. Candidate reference value is calulated by taking the
    difference of the normalized noun-phrases/keyword similarity value of both candidates.
    Sentiment value is calculated using NaiveBayes Classifier trained on movie review data.
    It then returns list of processed data.

    '''
    raw_ref_hil_datalist = []
    raw_ref_tru_datalist = []
    polarity_datalist = []
    analyzer_NB = NaiveBayesAnalyzer()
    for tweet_data in tweets_data:
        tweet_data = tweet_data.split(',')
        tweet_text = tweet_data[2]
        tweet_text = re.sub(r'pic.*$', '', tweet_text)
        tweet_text = re.sub(r'http.*$', '', tweet_text)
        tweet_text = tweet_text.replace("@", "")
        tweet_text = tweet_text.replace("#", "")
        tweet_text = tweet_text.replace("'", "")

        tweet_text_blob = TextBlob(tweet_text, analyzer=analyzer_NB)
        tweet_polarity = (tweet_text_blob.sentiment.p_pos*2.0) - 1.0
        tweet_ref_hil = max_noun_phrase_similarity(tweet_text, ["hillary clinton", "hillaryclinton"])
        tweet_ref_tru = max_noun_phrase_similarity(tweet_text, ["donald trump", "realdonaldtrump"])
        raw_ref_hil_datalist.append(tweet_ref_hil)
        raw_ref_tru_datalist.append(tweet_ref_tru)
        polarity_datalist.append(tweet_polarity)

    max_value_hil = max(raw_ref_hil_datalist)
    max_value_tru = max(raw_ref_tru_datalist)
    min_value_hil = min(raw_ref_hil_datalist)
    min_value_tru = min(raw_ref_tru_datalist)
    norm_ref_datalist = []
    for i in range(len(raw_ref_hil_datalist)):
        norm_ref = float(raw_ref_hil_datalist[i]-min_value_hil/max_value_hil - min_value_hil)-float(raw_ref_tru_datalist[i]-min_value_tru/max_value_tru - min_value_tru)
        norm_ref_datalist.append(norm_ref)
    processed_tweets_data = []
    for i in range(len(polarity_datalist)): processed_tweets_data.append([polarity_datalist[i], norm_ref_datalist[i]])
    return np.array(processed_tweets_data)

def max_noun_phrase_similarity(text, keywords):
    '''
    max_noun_phrase_similarity() finds string similarity between the keywords
    and the noun phrases of the text. It then returns the highest similarity value.

    '''
    noun_phrases = TextBlob(text).noun_phrases
    print(noun_phrases)
    values = []
    for keyword in keywords:
        for nf in noun_phrases: values.append(SequenceMatcher(None, keyword, nf).ratio())
    if len(values) == 0: return 0
    else: return max(values)

if __name__ == '__main__':
    ''''
    Parameters:
    parallel -set True to run distributed processing
    cores -number of cores used for distributed processing

    ''''
    parallel = False
    cores = 2

    '''
    Process all raw data files in data directory.

    '''
    for filename in sorted(os.listdir(path_to_data+"raw/")):
        tweets_data = []
        print("Processing: "+ filename)
        with open(path_to_data + filename, "r") as f: tweets_data = f.readlines()

        if parallel:
            tweets_data_parts = np.array_split(np.array(tweets_data),cores)
            tweets_data_parts = [sublist.tolist() for sublist in tweets_data_parts]
            with Pool() as pool:
                results = pool.map(process_tweet_data, tweets_data_parts)
            dataset = [val for sublist in results for val in sublist]
        else:
            dataset = process_tweet_data(tweets_data)

        os.makedirs(os.path.dirname(path_to_data+"processed/processed_"+filename), exist_ok=True)
        np.savetxt(path_to_data+"processed/processed_"+filename, dataset, fmt='%.5f', delimiter=",")
        print("Processing Done.\nProcessed File: processed_"+filename)
