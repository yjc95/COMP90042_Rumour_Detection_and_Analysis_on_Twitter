import json
import tweepy
import time
import pandas

class CrawlerConfig:
    # API_Key = 'CaOARF3tCzbfb9i85bYNpG2Ac'
    # API_Key_Secret = 'KuXILNgkz4im52FE7dweV2xn3LwtjtQCFGvup2dNVmLKiomQ5W'
    # Access_Token = '1084961461800189955-3AZbmwRsuKxwnoe9Cmb9UAgeC87pcY'
    # Access_Token_Secret = '64a43huJk9gYR0fKA1OvPbDXAZ1BUQoTVpNvLBFIOynAm'
    # Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAB2ucAEAAAAAhabe8%2F6r9PTdnfb506VKqQGSjS0%3DsEjcDzbkcrQCFxYqsTNf2IzJfAwlu4yK0xvkj2pDDPsJC4WznE'
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

# time.sleep(1000)

with open('./project-data/train.data.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        ids = line[:-2].split(',')
        # print(type(ids), ids)
        tweets = {}
        for id in ids:
            try:
                tweets[id] = client.get_tweets(ids=id,
                                               tweet_fields=['text', 'created_at', 'lang', 'geo', 'public_metrics'],
                                               user_fields=['public_metrics', 'description', 'created_at', 'location'],
                                               expansions=['author_id'])
            except Exception:
                time.sleep(3)
            count += 1
            if count == 445:
                print('450 tweets have been crawled!')
                count = 0
                time.sleep(1000)
        # print(type(tweets), tweets)
        line_number += 1
        print(line_number, 'lines have been crawled!')
        save(tweets, './project-data/tweet-train.txt')
