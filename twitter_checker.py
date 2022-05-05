import json
import tweepy
import time
import pandas

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


def load(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readline().strip()
        return json.loads(data)


auth = CrawlerConfig()

# start_time = time.time()

client = tweepy.Client(bearer_token=auth.Bearer_Token,
                       consumer_key=auth.API_Key,
                       consumer_secret=auth.API_Key_Secret,
                       access_token=auth.Access_Token,
                       access_token_secret=auth.Access_Token_Secret,
                       return_type=dict)

count = 0
line_number = 0
cannot_find = []

# time.sleep(1000)

with open('./project-data/train.data.txt', 'r', encoding='utf-8') as f1, open('./project-data/tweet-train.txt', 'r', encoding='utf-8') as f2:
    id_all = f1.readlines()
    tweet_all = f2.readlines()
    # ids = id_all[1][:-2].split(',')
    # tweets = json.loads(tweet_all[1])
    # print(type(ids), ids)
    # print('2' in tweets)
    # print(type(tweets), tweets['554893579957460992'])
    for i in range(1895):
        ids = id_all[i][:-2].split(',')
        tweets = json.loads(tweet_all[i])
        for id in ids:
            if id not in tweets:
                second = False
                while True:
                    try:
                        tweets[id] = client.get_tweets(ids=id,
                                                       tweet_fields=['text', 'created_at', 'lang', 'geo', 'public_metrics'],
                                                       user_fields=['public_metrics', 'description', 'created_at',
                                                                    'location'],
                                                       expansions=['author_id'])
                        break
                    except Exception:
                        if second:
                            cannot_find.append(id)
                        else:
                            print('Let crawler sleep for 16 mins!')
                            time.sleep(960)
                            second = True
            count += 1
        line_number += 1
        print(line_number, 'lines have been crawled!')
        save(tweets, './project-data/tweet-train-complete.txt')

print(count, 'tweets missing in the initial crawled data!')
print(len(cannot_find), 'tweets still cannot be crawled!')
print('These tweets still cannot be crawled: \n', cannot_find)