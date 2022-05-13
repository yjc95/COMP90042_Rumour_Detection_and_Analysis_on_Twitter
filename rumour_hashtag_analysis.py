"""
Analyse the hashtags
"""
import json
from nltk.tokenize import TweetTokenizer
import re

rumour_data = []
nonrumour_data = []


def data_tokenize(data):
    """
    Tokenize data

    :param data: text string list
    :return: the tokenized bag of words
    """
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
    """
    Get the uniques hashtags

    :param data:
    :return:
    """
    hashtag = set([])
    for d in data:
        for word, frequency in d.items():
            if word.startswith("#") and len(word) > 1:
                hashtag.add(word)
    return hashtag


def get_all_hashtags_freq(data):
    """
    Get the hashtag frequency

    :param data:
    :return:
    """
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

rumour_hashtags_freq = get_all_hashtags_freq(rumour_tokenized)
nonrumour_hashtags_freq = get_all_hashtags_freq(nonrumour_tokenized)
rumour_hashtags_freq_sorted = sorted(rumour_hashtags_freq.items(), key = lambda x: x[1], reverse=True)
nonrumour_hashtags_freq_sorted = sorted(nonrumour_hashtags_freq.items(), key = lambda x: x[1], reverse=True)
print("Number of hashtags in rumours =", len(rumour_hashtags_freq_sorted))
print(rumour_hashtags_freq_sorted[:10])
print("Number of hashtags in nonrumours =", len(nonrumour_hashtags_freq_sorted))
print(nonrumour_hashtags_freq_sorted[:10])
# Number of hashtags in rumours = 1419
# [('#covid19', 295), ('#coronavirus', 190), ('#trump', 33), ('#covid_19', 23), ('#wuhanvirus', 19), ('#covidー19', 19), ('#china', 19), ('#pandemic', 15), ('#coronaviruspandemic', 15), ('#covid', 13)]
# Number of hashtags in nonrumours = 20970
# [('#covid19', 7543), ('#coronavirus', 5261), ('#trump', 1089), ('#coronaviruspandemic', 801), ('#covidー19', 665), ('#covid_19', 662), ('#covid', 615), ('#trumpvirus', 593), ('#maga', 530), ('#wuhanvirus', 488)]

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
# Number of hashtags in rumours = 414
# [('#420day', 2), ('#thankyouforyourservice', 2), ('#ltgov', 1), ('#elected', 1), ('#appointed', 1), ('#criminally', 1), ('#civilrightsviolations', 1), ('#abuses', 1), ('#statutesoflimitations', 1), ('#dunningkruegereffect', 1)]
# Number of hashtags in nonrumours = 19965
# [('#coronavirusupdates', 96), ('#sarscov2', 94), ('#votebluenomatterwho', 87), ('#trumpisacompletefailure', 83), ('#kag2020', 79), ('#bluewave2020', 69), ('#trumprecession', 69), ('#stayhomestaysafe', 65), ("#trump's", 61), ('#trumppressconf', 59)]

count = 0

for hashtag in rumour_hashtags_unique:
    if hashtag in nonrumour_hashtags_unique:
        count += 1

print('The number of overlap hashtag is', count)
# The number of overlap hashtag is 1005
