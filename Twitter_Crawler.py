import tweepy
import time
import pandas

class CrawlerConfig:
    API_Key = 'CaOARF3tCzbfb9i85bYNpG2Ac'
    API_Key_Secret = 'KuXILNgkz4im52FE7dweV2xn3LwtjtQCFGvup2dNVmLKiomQ5W'
    Access_Token = '1084961461800189955-3AZbmwRsuKxwnoe9Cmb9UAgeC87pcY'
    Access_Token_Secret = '64a43huJk9gYR0fKA1OvPbDXAZ1BUQoTVpNvLBFIOynAm'
    Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAB2ucAEAAAAAhabe8%2F6r9PTdnfb506VKqQGSjS0%3DsEjcDzbkcrQCFxYqsTNf2IzJfAwlu4yK0xvkj2pDDPsJC4WznE'





auth = CrawlerConfig()

start_time = time.time()

client =tweepy.Client(bearer_token=auth.Bearer_Token,
                      consumer_key= auth.API_Key,
                      consumer_secret=auth.API_Key_Secret,
                      access_token=auth.Access_Token,
                      access_token_secret= auth.Access_Token_Secret,
                      return_type=dict).get_tweets('80080680482123777',tweet_fields=["text"])




print(client)

