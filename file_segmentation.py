import json


def save(content, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)


with open('./project-data/covid.data.txt', 'r', encoding='utf-8') as f:
    id_all = f.readlines()
    for i in range(0, 2000):
        save(id_all[i], './project-data/covid-pt1.txt')
    for i in range(2000, 4000):
        save(id_all[i], './project-data/covid-pt2.txt')
    for i in range(4000, 6000):
        save(id_all[i], './project-data/covid-pt3.txt')
    for i in range(6000, 8000):
        save(id_all[i], './project-data/covid-pt4.txt')
    for i in range(8000, 10000):
        save(id_all[i], './project-data/covid-pt5.txt')
    for i in range(10000, 12000):
        save(id_all[i], './project-data/covid-pt6.txt')
    for i in range(12000, 14000):
        save(id_all[i], './project-data/covid-pt7.txt')
    for i in range(14000, 16000):
        save(id_all[i], './project-data/covid-pt8.txt')
    for i in range(16000, 17458):
        save(id_all[i], './project-data/covid-pt9.txt')
