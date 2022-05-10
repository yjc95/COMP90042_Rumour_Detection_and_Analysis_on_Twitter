import json


def save(dict, file_path):
    if isinstance(dict, str):
        dict = eval(dict)
    with open(file_path, 'a', encoding='utf-8') as f:
        str_ = json.dumps(dict, ensure_ascii=False)
        f.write(str_)
        f.write('\n')


line_number = 0
cannot_find = []

with open('./project-data/tweet-covid-pt9-raw.txt', 'r', encoding='utf-8') as f1, \
        open('./project-data/covid-pt9.txt', 'r', encoding='utf-8') as f2:
    tweet_all = f1.readlines()
    print(len(tweet_all), 'lines in total!')
    id_all = f2.readlines()

    data = {}
    user = {}
    for tweets_json in tweet_all:
        tweets_ini = json.loads(tweets_json)
        for i in range(len(tweets_ini['data'])):
            data[tweets_ini['data'][i]['id']] = tweets_ini['data'][i]
        for i in range(len(tweets_ini['includes']['users'])):
            data[tweets_ini['includes']['users'][i]['id']] = tweets_ini['includes']['users'][i]

    for ids in id_all:
        ids = ids[:-1].split(',')
        tweets = {}
        for id in ids:
            if id in data:
                author_id = data[id]['author_id']
                if author_id in user:
                    user_part = user[author_id]
                else:
                    user_part = {}
                tweets[id] = {'data': [data[id]], 'includes': {'users': [user_part]}}
            else:
                cannot_find.append([line_number+1, id])
        line_number += 1
        print(line_number, 'lines have been decoded!')
        save(tweets, './project-data/tweet-covid-pt9.txt')

print(len(cannot_find), 'tweets cannot be found!')
print('These tweets cannot be found: \n', cannot_find)

