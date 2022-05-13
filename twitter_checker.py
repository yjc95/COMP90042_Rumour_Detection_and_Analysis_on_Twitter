"""
Tweet checker for missing data
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

count = 0
line_number = 0
cannot_find = []


def check_id(id_file_path, data_file_path):
    count = 0
    with open(id_file_path, 'r', encoding='utf-8') as f1, open(data_file_path, 'r', encoding='utf-8') as f2:
        id_all = f1.readlines()
        tweet_all = f2.readlines()
        for i in range(len(id_all)):
            ids = id_all[i][:-1].split(',')
            tweets_ini = json.loads(tweet_all[i])
            for j in range(len(ids)):
                if ids[j] not in tweets_ini:
                    count += 1
    return count


with open('./project-data/dev.data.txt', 'r', encoding='utf-8') as f1, open('./project-data/tweet-dev-complete.txt', 'r', encoding='utf-8') as f2:
    id_all = f1.readlines()
    tweet_all = f2.readlines()
    for i in range(len(id_all)):
        ids = id_all[i][:-1].split(',')
        tweets_ini = json.loads(tweet_all[i])
        tweets = {}
        for j in range(len(ids)-1):
            if ids[j] in tweets_ini:
                tweets[ids[j]] = tweets_ini[ids[j]]
            else:
                second = False
                while True:
                    try:
                        tweets[ids[j]] = client.get_tweets(ids=ids[j],
                                                           tweet_fields=['text', 'created_at', 'lang', 'geo',
                                                                          'public_metrics'],
                                                           user_fields=['public_metrics', 'description', 'created_at',
                                                                         'location'],
                                                           expansions=['author_id'])
                        break
                    except Exception:
                        if second:
                            cannot_find.append(ids[j])
                            break
                        else:
                            print('Let crawler sleep for 16 mins!')
                            time.sleep(960)
                            second = True

        last_id = ids[len(ids)-1]
        second = False
        while True:
            try:
                tweets[last_id] = client.get_tweets(ids=last_id,
                                                    tweet_fields=['text', 'created_at', 'lang', 'geo', 'public_metrics'],
                                                    user_fields=['public_metrics', 'description', 'created_at', 'location'],
                                                    expansions=['author_id'])
                break
            except Exception:
                if second:
                    cannot_find.append(last_id)
                else:
                    print('Let crawler sleep for 16 mins!')
                    time.sleep(960)
                    second = True
        line_number += 1
        print(line_number, 'lines have been crawled!')
        save(tweets, './project-data/tweet-dev-final.txt')

print(len(cannot_find), 'tweets still cannot be crawled!')
print('These tweets still cannot be crawled: \n', cannot_find)
