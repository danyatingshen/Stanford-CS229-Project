
from collections import defaultdict

# For two , four digit numbers, there are a total of (10,0000)^2 permutations of problems
#Start Small and progressively increase the maxnum
MAX_NUM = 50

bins = defaultdict(lambda: [])

def feature_extractor(val_1, val_2):

    num_1_digit = len(str(val_1))
    num_2_digit = len(str(val_2))

    feature = (num_1_digit, num_2_digit)
    return feature


for num_1 in range(0, MAX_NUM + 1):
    for num_2 in range(0, MAX_NUM + 1):

        key = feature_extractor(num_1, num_2)
        print("Problem: " + str(num_1) + " + " + str(num_2) + " = ? is mapped to feature space as: " + str(key) )

        bins[key].append((num_1, num_2))


# Bin statistics
for key in bins:
    print("Bin Name: " + str(key) + "   Bin Count: " + str(len(bins[key])))
    print(bins[key])
    print("")
