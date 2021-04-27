
from collections import defaultdict
import math

# For two , four digit numbers, there are a total of (10,0000)^2 permutations of problems
#Start Small and progressively increase the maxnum
MAX_NUM = 999

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


    if int(val_1) ==0 or int(val_2) == 0:
        zero_count = 'base'
        num_1_digit = 'base'
        num_2_digit = 'base'
        carry_ops = 'base'

    #Count not leading zeros

    feature = (num_1_digit, num_2_digit, carry_ops, zero_count)
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

for key in bins:
    print("Bin Name: " + str(key) + "   Bin Count: " + str(len(bins[key])))
    print( bins[key][0:100])
    print("")



