
from collections import defaultdict
import math
import ujson
import json

# For two , four digit numbers, there are a total of (10,0000)^2 permutations of problems
#Start Small and progressively increase the maxnum
MAX_NUM = 99

bins = defaultdict(lambda: [])

def num_carry_ops(val_1, val_2):

    num1_str = str(val_1)
    num1_str = num1_str[::-1]

    num2_str = str(val_2)
    num2_str = num2_str[::-1]
    i = 0
    j = 0
    carry_val = 0
    carry_count = 0

    while (i < len(num1_str) or j < len(num2_str)):
        x = 0
        y = 0

        if (i < len(num1_str)):
            x = int(num1_str[i]) #+ int('0');
            i += 1

        if (j < len(num2_str)):
            y = int(num2_str[j]) #+ int('0');
            j += 1

        currentVal = x + y + carry_val

        if currentVal >= 10:
            carry_count += 1
            carry_val = math.floor(currentVal/10)

    return carry_count

def count_zeros(val_1, val_2):

    zero_count_1 = str(val_1).count('0')
    zero_count_2 = str(val_2).count('0')

    return zero_count_1 + zero_count_2

def non_trailing_zero_count(val_1, val_2):

    total_zero_1 = str(val_1).count('0')
    total_zero_2 = str(val_2).count('0')

    num1_str = str(val_1)
    num2_str = str(val_2)

    trail_1 = len(num1_str) - len(num1_str.rstrip('0'))
    trail_2 = len(num2_str) - len(num2_str.rstrip('0'))

    return ((len(num1_str) - trail_1) == 1  and  (len(num2_str) - trail_2) == 1  and val_1 != 0 and val_2 != 0 and total_zero_1 != 0 and total_zero_2 != 0)

def feature_extractor(val_1, val_2):
    #val2 will always be larger than val1
    if val_1 > val_2:
        temp = val_1
        val_1 = val_2
        val_2 = temp

    carry_ops = num_carry_ops(val_1,val_2)
    zero_count = count_zeros(val_1, val_2)

    num_1_digit = len(str(val_1))
    num_2_digit = len(str(val_2))

    #Count not leading zeros
    trail = non_trailing_zero_count(val_1, val_2)
    if trail:
        isTrail = 'trailTrue'
        zero_count = 'trailed'
        num_1_digit = 'trailed'
        num_2_digit = 'trailed'

    else:
        isTrail = 'trailFalse'

    if int(val_1) ==0 or int(val_2) == 0:
        num_1_digit = 'baseCase'
        num_2_digit = 'baseCase'
        carry_ops   = 'baseCase'
        zero_count  = 'baseCase'

    feature = (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)

    return feature


for num_1 in range(0, MAX_NUM + 1):
    for num_2 in range(0, MAX_NUM + 1):

        key = feature_extractor(num_1, num_2)
        #print("Problem: " + str(num_1) + " + " + str(num_2) + " = ? is mapped to feature space as: " + str(key) )

        bins[key].append((num_1, num_2))

# Bin statistics
print("Total number of math problems: " + str( (MAX_NUM+1) ** 2) )
print("Total number of bins: " + str( len(bins) ) )
print("")

"""
for key in bins:
    print("Bin Name: " + str(key) + "   Bin Count: " + str(len(bins[key])))
    print( bins[key][0:100])
    print("")

"""

#with open('dict_temp.txt', 'w') as file:
#    file.write(ujson.dumps(bins))

temp = json.load( open('dict_temp.txt', 'r') )

for key in temp:
    print("Bin Name: " + str(key) + "   Bin Count: " + str(len(bins[key])))
    print( bins[key][0:100])
    print("")