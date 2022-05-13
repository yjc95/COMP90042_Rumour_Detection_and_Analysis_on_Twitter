"""
Twitter data crawler
"""
import json
import tweepy
import time


class CrawlerConfig:
    API_Key = "EnDNAmWMuYdkG8yDNoyNNrbxN"
    API_Key_Secret = "4ogFecdNh6UYcIAZGxJSwODKRu5NyjKHYr1HrjGygeMlS7Ws7y"
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAFaQcAEAAAAAkIcOhCiC8zeiSoOwW9iPgz%2Busa4%3DI0SvisQA1BrYnp9HbNrcbqE3ZvrX8nCGv5SUrMFxEXNIfobE3O"
    Access_Token = "1521167251558531073-yawqcgPH1h5ESrTtyRhrLpqNLorM1I"
    Access_Token_Secret = "T0A3eQu6T6bAfjj9JNed773DOL26tGD5pUGxUPBYZYZWh"


def save(dict, file_path):
    if isinstance(dict, str):
        dict = eval(dict)
    with open(file_path, 'a', encoding='utf-8') as f:
        str_ = json.dumps(dict, ensure_ascii=False)
        f.write(str_)
        f.write('\n')


auth = CrawlerConfig()

client = tweepy.Client(bearer_token=auth.Bearer_Token,
                       consumer_key=auth.API_Key,
                       consumer_secret=auth.API_Key_Secret,
                       access_token=auth.Access_Token,
                       access_token_secret=auth.Access_Token_Secret,
                       return_type=dict)

line_number = 0
cannot_find = []

id_list = []
id_list_temp = []

# Open the id list waiting for crawling
with open('./project-data/covid-pt4.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        ids = line[:-1].split(',')
        tweets = {}
        for id in ids:
            id_list_temp.append(id)
            if len(id_list_temp) >= 100:
                id_list.append(id_list_temp)
                id_list_temp = []

id_list.append(id_list_temp)

# print(id_list[0])
# print(id_list[len(id_list)-1])
print('The total line number is', len(id_list))
# print(len(id_list[0]))
# print(len(id_list[len(id_list)-1]))

for ids in id_list:
    second = False
    while True:
        try:
            tweets = client.get_tweets(ids=ids,
                                       tweet_fields=['text', 'created_at', 'lang', 'geo', 'public_metrics'],
                                       user_fields=['public_metrics', 'description', 'created_at', 'location'],
                                       expansions=['author_id'])
            break
        except Exception:
            if second:
                cannot_find.append(ids)
                break
            else:
                print('Let crawler sleep for 16 mins!')
                time.sleep(960)
                second = True
    line_number += 1
    print(line_number, 'lines have been crawled!')
    save(tweets, './project-data/tweet-covid-pt4-raw.txt')

# The raw data needs a decoder to return to the same format of the id list

print(len(cannot_find), 'tweets cannot be crawled!')
print('These tweets cannot be crawled: \n', cannot_find)
