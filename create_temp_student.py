import FeatureExtractor
import util
import ujson
import random
import pprint
bins = ujson.load(open('data/problemBank.json', 'r'))

student = {}
for key in bins:
    if random.random() < .2:
        correct = -1
    else:
        correct = 1
    student[key] = [correct*random.random()*100, random.random()*10]

student.pop('num_states', None)
student.pop('state_limit', None)

pprint.pprint(student, width=1)

util.save_q("data/rand_student.json", student)
