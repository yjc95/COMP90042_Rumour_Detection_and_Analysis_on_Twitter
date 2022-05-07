import json
import nltk
from nltk.tokenize import TweetTokenizer
# nltk.download('stopwords')
# from nltk.corpus import stopwords
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import csv

x_train_data, x_dev_data, x_test_data = [], [], []
y_train_data, y_dev_data = [], []

with open('./project-data/tweet-train-final.txt', 'r', encoding='utf-8') as f:
    tweet_all = f.readlines()
    # tweet = json.loads(tweet_all[0])
    # print(type(tweet['1250219300389974016']['data'][0]['text']), tweet['1250219300389974016']['data'][0]['text'])
    for event in tweet_all:
        # print(type(tweets), tweets)
        tweets = json.loads(event)
        text_event = ''
        for k, v in tweets.items():
            if 'data' in v:
                text_event += v['data'][0]['text']
        x_train_data.append(text_event)

with open('./project-data/train.label.txt', 'r', encoding='utf-8') as f:
    label_all = f.readlines()
    # print(type(label_all[1][:-1]), label_all[1][:-1])
    for label in label_all:
        if label[:-1] == 'rumour':
            y_train_data.append(1)
        else:
            y_train_data.append(0)

with open('./project-data/tweet-dev-final.txt', 'r', encoding='utf-8') as f:
    tweet_all = f.readlines()
    for event in tweet_all:
        tweets = json.loads(event)
        text_event = ''
        for k, v in tweets.items():
            if 'data' in v:
                text_event += v['data'][0]['text']
        x_dev_data.append(text_event)

with open('./project-data/dev.label.txt', 'r', encoding='utf-8') as f:
    label_all = f.readlines()
    for label in label_all:
        if label[:-1] == 'rumour':
            y_dev_data.append(1)
        else:
            y_dev_data.append(0)

with open('./project-data/test.data.txt', 'r', encoding='utf-8') as f:
    id_all = f.readlines()
    for i in range(len(id_all)):
        ids = id_all[i][:-1].split(',')
        text_event = ''
        for j in range(len(ids)):
            file_path = './project-data/tweet-objects/' + ids[j] + '.json'
            # try:
            with open(file_path, 'r', encoding='utf-8') as f2:
                tweet = json.load(f2)
                text_event += tweet['text']
            # except Exception:
            #     pass
        x_test_data.append(text_event)

# print("Number of tweets =", len(x_train_data))
# print("Number of labels =", len(y_train_data))
# print("\nSamples of data:")
# for i in range(5):
#     print("Label =", y_train_data[i], "\tTweet =", x_train_data[i])
# print("Number of tweets =", len(x_dev_data))
# print("Number of labels =", len(y_dev_data))
# print("\nSamples of data:")
# for i in range(5):
#     print("Label =", y_dev_data[i], "\tTweet =", x_dev_data[i])
# print("Number of tweets =", len(x_test_data))
# print("\nSamples of data:")
# for i in range(5):
#     print("Tweet =", x_test_data[i])


def preprocess_data(data, labels):
    tt = TweetTokenizer()
    stopwords = set(nltk.corpus.stopwords.words('english'))  # note: stopwords are all in lowercase
    processed_x = []
    processed_y = []

    for i in range(len(data)):
        tweet = data[i]
        init_token = tt.tokenize(tweet)
        token = []
        for j in range(len(init_token)):
            init_token[j] = init_token[j].lower()
            if re.search('[a-z]', init_token[j]) and init_token[j] not in stopwords and not re.match('^http[s]?://.*', init_token[j]):
                token.append(init_token[j])
        BOW = {}
        for word in token:
            BOW[word] = BOW.get(word, 0) + 1
        if len(token) != 0:
            processed_x.append(BOW)
            if i < len(labels):
                processed_y.append(labels[i])

    return [processed_x, processed_y]


x_train_processed, y_train = preprocess_data(x_train_data, y_train_data)
x_dev_processed, y_dev = preprocess_data(x_dev_data, y_dev_data)
x_test_processed, _ = preprocess_data(x_test_data, [])

# print("Number of preprocessed tweets =", len(x_train_processed))
# print("Number of preprocessed labels =", len(y_train))
# print("\nSamples of preprocessed data:")
# for i in range(5):
#     print("Country =", y_train[i], "\tTweet =", x_train_processed[i])
# print("Number of preprocessed tweets =", len(x_dev_processed))
# print("Number of preprocessed labels =", len(y_dev))
# print("\nSamples of preprocessed data:")
# for i in range(5):
#     print("Country =", y_dev[i], "\tTweet =", x_dev_processed[i])
# print("Number of preprocessed tweets =", len(x_test_processed))
# print("\nSamples of preprocessed data:")
# for i in range(5):
#     print("Tweet =", x_test_processed[i])


# def get_all_hashtags(data):
#     hashtag = set([])
#     for d in data:
#         for word, frequency in d.items():
#             if word.startswith("#") and len(word) > 1:
#                 hashtag.add(word)
#     return hashtag
#
#
# hashtags = get_all_hashtags(x_processed)
# print("Number of hashtags =", len(hashtags))
# print(sorted(hashtags))

vectorizer = DictVectorizer()
x_train = vectorizer.fit_transform(x_train_processed)
x_dev = vectorizer.transform(x_dev_processed)
x_test = vectorizer.transform(x_test_processed)

# alpha_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# for a in alpha_list:
#     nb = MultinomialNB(alpha=a)
#     nb.fit(x_train, y_train)
#     print("The accuracy of Naive Bayes Classifier with alpha =", end=" ")
#     print(a, "is", round(nb.score(x_dev, y_dev), 5) * 100, "%")
#
# C_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# for c in C_list:
#     lr = LogisticRegression(C=c)
#     lr.fit(x_train, y_train)
#     print("The accuracy of Logistic Regression Classifier with C =", end=" ")
#     print(c, "is", round(lr.score(x_dev, y_dev), 5) * 100, "%")

nb = MultinomialNB(alpha=0.9)
nb.fit(x_train, y_train)
print("The accuracy of Naive Bayes Classifier with alpha = 0.9 is", round(nb.score(x_dev, y_dev), 5) * 100, "%")

lr = LogisticRegression(C=0.7)
lr.fit(x_train, y_train)
print("The accuracy of Logistic Regression Classifier with C = 0.7 is", round(lr.score(x_dev, y_dev), 5) * 100, "%")

nb_y_pred = nb.predict(x_test)
lr_y_pred = lr.predict(x_test)

with open('./project-data/bayes-predict.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['Id', 'Predicted']
    writer.writerow(header)
    for i in range(len(nb_y_pred)):
        data = [i, nb_y_pred[i]]
        writer.writerow(data)

with open('./project-data/logistic-predict.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['Id', 'Predicted']
    writer.writerow(header)
    for i in range(len(lr_y_pred)):
        data = [i, lr_y_pred[i]]
        writer.writerow(data)
