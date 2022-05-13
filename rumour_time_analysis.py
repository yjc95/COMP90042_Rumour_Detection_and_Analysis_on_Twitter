"""
Analysis tweeting time
"""
import json
from utils import save_csv

rumour_time_count = [0 for i in range(24)]
nonrumour_time_count = [0 for i in range(24)]
rumour_month_count = [0 for i in range(12)]
nonrumour_month_count = [0 for i in range(12)]
rumour_date_count = {}
nonrumour_date_count = {}

# Load tweet time count
with open('./tweet_covid_result_bert.csv', 'r', encoding='utf-8') as f1, \
        open('./project-data/tweet-covid-final.txt', 'r', encoding='utf-8') as f2, \
        open('./project-data/covid.data.txt', 'r', encoding='utf-8') as f3:
    result_all = f1.readlines()
    tweet_all = f2.readlines()
    id_all = f3.readlines()
    for i in range(len(id_all)):
        id = id_all[i][:-1].split(',')[0]
        tweets = json.loads(tweet_all[i])
        if id not in tweets or 'created_at' not in tweets[id]['data'][0]:
            continue
        created_at = tweets[id]['data'][0]['created_at']
        # created_at = "2020-04-15T00:28:03.000Z"
        if len(created_at) == 0:
            continue
        month = int(created_at[5:7])
        hour = int(created_at[11:13])
        date = created_at[0:10]
        if int(result_all[i+1][:-1].split(',')[1]):
            rumour_time_count[hour] += 1
            rumour_month_count[month] += 1
            rumour_date_count[date] = rumour_date_count.get(date, 0) + 1
        else:
            nonrumour_time_count[hour] += 1
            nonrumour_month_count[month] += 1
            nonrumour_date_count[date] = nonrumour_date_count.get(date, 0) + 1

save_csv(['hour', 'rumour', 'nonrumour'], './project-data/rumour_time_count.csv')
for i in range(24):
    save_csv([i, rumour_time_count[i], nonrumour_time_count[i]], './project-data/rumour_time_count.csv')

save_csv(['month', 'rumour', 'nonrumour'], './project-data/rumour_month_count.csv')
for i in range(12):
    save_csv([i, rumour_month_count[i], nonrumour_month_count[i]], './project-data/rumour_month_count.csv')

rumour_date_sorted = sorted(rumour_date_count)
save_csv(['date', 'rumour'], './project-data/rumour_date_count.csv')
for date in rumour_date_sorted:
    save_csv([date, rumour_date_count[date]], './project-data/rumour_date_count.csv')
nonrumour_date_sorted = sorted(nonrumour_date_count)
save_csv(['date', 'nonrumour'], './project-data/nonrumour_date_count.csv')
for date in nonrumour_date_sorted:
    save_csv([date, nonrumour_date_count[date]], './project-data/nonrumour_date_count.csv')

print('Total rumour:', sum(rumour_time_count))
print('Total nonrumour:', sum(nonrumour_time_count))

print('rumour_time_count:', rumour_time_count)
print('nonrumour_time_count:', nonrumour_time_count)

print('rumour_month_count:', rumour_month_count)
print('nonrumour_month_count:', nonrumour_month_count)

print('rumour_date_count:', sorted(rumour_date_count))
print('nonrumour_date_count:', sorted(nonrumour_date_count))
