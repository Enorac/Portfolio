import social_tests as test
import pandas as pd
import numpy as np
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
### STAGE 1 ###

def parse_label(label):
    d = {}
    endname = label.find('(')
    d["name"] = label[6:endname-1]
    endpos = label.find('from')
    d['position'] = label[endname+1:endpos-1]
    d['state'] = label[endpos+5:-1]
    return d

def get_region_from_state(state_df, state):
    result = state_df[state_df['state']==state]
    return result.iloc[0]["region"]

import copy
end_chars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]
def find_hashtags(message):
    lst = []
    for i in range(len(message)):
      if message[i] == '#':
        j = i+1
        while j < len(message) and message[j] not in end_chars:
          j += 1
        lst.append(message[i:j])
    return lst

def find_sentiment(classifier,message):
    score = classifier.polarity_scores(message)['compound']
    if score > .1:
      rating = 'positive'
    elif score < -.1:
      rating = 'negative'
    elif score < .1 and score > -.1:
      rating = 'neutral'
    return (score,rating)

def add_columns(data, state_df):
    classifier = SentimentIntensityAnalyzer()
    names, positions, states, regions = [],[],[],[]
    for i in data['label']:
      d = parse_label(i)
      names.append(d['name'])
      positions.append(d['position'])
      states.append(d['state'])
      regions.append(get_region_from_state(state_df,d['state']))
    data['name'] = names
    data['position'] = positions
    data['state'] = states
    data['region'] = regions

    hashtags, scores, sentiments = [],[],[]
    for i in data['text']:
      hashtags.append(find_hashtags(i))
      scores.append(find_sentiment(classifier,i)[0])
      sentiments.append(find_sentiment(classifier,i)[1])
    data['score'] = scores
    data['hashtags'] = hashtags
    data['sentiment'] = sentiments

### PHASE 2 ###

def get_sentiment_quantiles(data, col_name, col_value):
    if col_name != '':
      data = data[data[col_name] == col_value]
    result = [data['score'].min()]
    result.extend(list(data['score'].quantile([.25,.50,.75])))
    result.append(data['score'].max())
    return result

def get_hashtag_subset(data, col_name, col_value):
    if col_name != '':
      data = data[data[col_name] == col_value]
    result = set()
    hash = []
    for i in data['hashtags']:
      for j in i:
        if j != '' and j not in hash:
          hash.append(j)
    return hash

def get_hashtag_rates(data):
    d = {}
    for i in data['hashtags']:
      for j in i:
        if j in d.keys():
          d[j] = d[j] + 1
        else:
          d[j] = 1
    return d

def most_common_hashtags(hashtags, count):
    result = {}
    lst = []
    for i in hashtags.items():
      lst.append(i[1])
    lst.sort()
    lst = lst[-count:]
    for i in hashtags:
      if hashtags[i] in lst:
        lst.pop(lst.index(hashtags[i]))
        result[i] = hashtags[i]
    return result

def get_hashtag_sentiment(data, hashtag):
    count = 0
    total = 0
    for i, r in data.iterrows():
      hashtags = r['hashtags']
      sentiment = r['sentiment']
      if hashtag in hashtags:
        count += 1
        if sentiment == 'positive':
          total += 1
        elif sentiment == 'negative':
          total -= 1
    return total/count

### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    test.test_all()
    test.run()