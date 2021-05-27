import util
import numpy as np

amanda = util.load_student('data_amshen.txt')
takara = util.load_student('data_takara.txt')
cortney = util.load_student('data_cortney.txt')

student = takara
student_save = {}

avg_list = []
for key in student:
    data = np.asarray(student[key])
    avg_list.append(abs(data).mean())
max_avg = max(avg_list)

for key in student:
    data = np.asarray(student[key])/max_avg
    avg = abs(data).mean()
    std = abs(data).std()
    correct = data[np.where(data > 0)]
    percent_wrong = (len(data) - len(correct)) / len(data)

    student_save[key] = [avg, std, percent_wrong]

util.save_q('student_takara_norm.json', student_save)

