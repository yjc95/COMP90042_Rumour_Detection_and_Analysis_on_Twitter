import json
import tweepy
import time
import pandas


class CrawlerConfig:
    API_Key = 'CaOARF3tCzbfb9i85bYNpG2Ac'
    API_Key_Secret = 'KuXILNgkz4im52FE7dweV2xn3LwtjtQCFGvup2dNVmLKiomQ5W'
    Access_Token = '1084961461800189955-3AZbmwRsuKxwnoe9Cmb9UAgeC87pcY'
    Access_Token_Secret = '64a43huJk9gYR0fKA1OvPbDXAZ1BUQoTVpNvLBFIOynAm'
    Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAB2ucAEAAAAAhabe8%2F6r9PTdnfb506VKqQGSjS0%3DsEjcDzbkcrQCFxYqsTNf2IzJfAwlu4yK0xvkj2pDDPsJC4WznE'


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

time.sleep(1000)

with open('./project-data/train.data.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        ids = line[:-2].split(',')
        # print(type(ids), ids)
        tweets = {}
        for id in ids:
            tweets[id] = client.get_tweets(ids=id,
                                           tweet_fields=['text', 'created_at', 'lang', 'geo', 'public_metrics'],
                                           user_fields=['public_metrics', 'description', 'created_at', 'location'],
                                           expansions=['author_id'])
            count += 1
            if count == 450:
                print('450 tweets have been crawled!')
                time.sleep(1000)
        # print(type(tweets), tweets)
        line_number += 1
        print(line_number, 'lines have been crawled!')
        save(tweets, './project-data/tweet-train.txt')
