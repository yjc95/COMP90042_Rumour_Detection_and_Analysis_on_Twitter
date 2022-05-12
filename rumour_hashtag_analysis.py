import json
import nltk
from nltk.tokenize import TweetTokenizer
import re

rumour_data = []
nonrumour_data = []


def data_tokenize(data):
    tt = TweetTokenizer()
    processed_x = []

    for i in range(len(data)):
        tweet = data[i]
        init_token = tt.tokenize(tweet)
        token = []
        for j in range(len(init_token)):
            init_token[j] = init_token[j].lower()
            if not re.match('^http[s]?://.*', init_token[j]):
                token.append(init_token[j])
        BOW = {}
        for word in token:
            BOW[word] = BOW.get(word, 0) + 1
        processed_x.append(BOW)

    return processed_x


def get_all_hashtags_unique(data):
    hashtag = set([])
    for d in data:
        for word, frequency in d.items():
            if word.startswith("#") and len(word) > 1:
                hashtag.add(word)
    return hashtag


def get_all_hashtags_freq(data):
    hashtag_freq = {}
    for d in data:
        for word, frequency in d.items():
            if word.startswith("#") and len(word) > 1:
                hashtag_freq[word] = hashtag_freq.get(word, 0) + 1
    return hashtag_freq


with open('./tweet_covid_result_bert.csv', 'r', encoding='utf-8') as f1, \
        open('./project-data/tweet-covid-final.txt', 'r', encoding='utf-8') as f2, \
        open('./project-data/covid.data.txt', 'r', encoding='utf-8') as f3:
    result_all = f1.readlines()
    tweet_all = f2.readlines()
    id_all = f3.readlines()
    for i in range(len(id_all)):
        ids = id_all[i][:-1].split(',')
        tweets = json.loads(tweet_all[i])
        text_event = ''
        for id in ids:
            if id not in tweets or 'created_at' not in tweets[id]['data'][0]:
                continue
            text_event += tweets[id]['data'][0]['text']

        if int(result_all[i+1][:-1].split(',')[1]):
            rumour_data.append(text_event)
        else:
            nonrumour_data.append(text_event)

rumour_tokenized = data_tokenize(rumour_data)
nonrumour_tokenized = data_tokenize(nonrumour_data)

rumour_hashtags_unique = get_all_hashtags_unique(rumour_tokenized)
nonrumour_hashtags_unique = get_all_hashtags_unique(nonrumour_tokenized)
# print("Number of hashtags in rumours =", len(rumour_hashtags_unique))
# print(sorted(rumour_hashtags_unique))
# print("Number of hashtags in nonrumours =", len(nonrumour_hashtags_unique))
# print(sorted(nonrumour_hashtags_unique))

rumour_hashtags_freq = get_all_hashtags_freq(rumour_tokenized)
nonrumour_hashtags_freq = get_all_hashtags_freq(nonrumour_tokenized)
rumour_hashtags_freq_sorted = sorted(rumour_hashtags_freq.items(), key = lambda x: x[1], reverse=True)
nonrumour_hashtags_freq_sorted = sorted(nonrumour_hashtags_freq.items(), key = lambda x: x[1], reverse=True)
print("Number of hashtags in rumours =", len(rumour_hashtags_freq_sorted))
print(rumour_hashtags_freq_sorted[:10])
print("Number of hashtags in nonrumours =", len(nonrumour_hashtags_freq_sorted))
print(nonrumour_hashtags_freq_sorted[:10])
# Number of hashtags in rumours = 1631
# [('#covid19', 247), ('#coronavirus', 197), ('#trump', 50), ('#china', 30), ('#wuhanvirus', 26), ('#trumpvirus', 25), ('#covid_19', 24), ('#maga', 22), ('#covidー19', 19), ('#coronaviruspandemic', 19)]
# Number of hashtags in nonrumours = 20848
# [('#covid19', 7591), ('#coronavirus', 5254), ('#trump', 1072), ('#coronaviruspandemic', 797), ('#covidー19', 665), ('#covid_19', 661), ('#covid', 614), ('#trumpvirus', 581), ('#maga', 521), ('#wuhanvirus', 481)]

rumour_hashtags_only = []
nonrumour_hashtags_only = []

for hashtag in rumour_hashtags_freq_sorted:
    if hashtag[0] not in nonrumour_hashtags_unique:
        rumour_hashtags_only.append(hashtag)

for hashtag in nonrumour_hashtags_freq_sorted:
    if hashtag[0] not in rumour_hashtags_unique:
        nonrumour_hashtags_only.append(hashtag)

print("Number of hashtags in rumours =", len(rumour_hashtags_only))
print(rumour_hashtags_only[:10])
print("Number of hashtags in nonrumours =", len(nonrumour_hashtags_only))
print(nonrumour_hashtags_only[:10])
# Number of hashtags in rumours = 536
# [('#redrobin', 2), ('#420day', 2), ('#antiamerican', 2), ('#istandwiththepresident', 1), ('#ppetochina', 1), ('#economyshutdown', 1), ('#followthedata', 1), ('#ili', 1), ('#hawleysgermwarfare', 1), ('#easterinfected', 1)]
# Number of hashtags in nonrumours = 19753
# [('#stayhomesavelives', 141), ('#uk', 110), ('#fakepresident', 105), ('#brexit', 80), ('#covid19uk', 80), ('#indiafightscorona', 70), ('#flattenthecurve', 69), ('#notmypresident', 67), ('#wethepeople', 66), ('#bunkerbitch', 59)]

count = 0

for hashtag in rumour_hashtags_unique:
    if hashtag in nonrumour_hashtags_unique:
        count += 1

print('The number of overlap hashtag is', count)
# The number of overlap hashtag is 1095
