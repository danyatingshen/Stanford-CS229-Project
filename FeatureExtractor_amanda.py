
from collections import defaultdict
import matplotlib.pyplot as plt

# For two , four digit numbers, there are a total of (10,0000)^2 permutations of problems
#Start Small and progressively increase the maxnum

# digit 
# number of 0 
# caret 



def feature_extractor(val_1, val_2):

    if val_1 > val_2:
        temp = val_1
        val_1 = val_2
        val_2 = temp

    trail = non_trailing_zero_count(val_1, val_2)
    tot_digits = total_number_digit(val_1, val_2)
    dif_digits = digit_diff(val_1, val_2)
    num_carry = number_of_carry(val_1, val_2)
    num_zero = number_of_zero(val_1,val_2)

    if trail:
        num_zero = 'trailed'
        tot_digits = 'trailed'
        dif_digits = 'trailed'
    else:
        trail = 'trailFalse'

    if (val_1 == 0 or val_2 == 0) or (val_1 == 1 or val_2 == 1):
        num_1_digit = 'baseCase'
        num_2_digit = 'baseCase'
        #num_carry = 'baseCase'
        tot_digits = 'baseCase'
        dif_digits = 'baseCase'
        num_zero = 'baseCase'

    #feature = (total_number_digit(val_1, val_2), digit_diff(val_1, val_2), is_same_number(val_1, val_2), number_of_carry(val_1, val_2), number_of_zero(val_1, val_2))
    #feature = (number_of_digit(val_1),number_of_digit(val_2), is_same_number(val_1, val_2), number_of_carry(val_1, val_2), number_of_zero(val_1, val_2))
    
    #feature = (total_number_digit(val_1, val_2), digit_diff(val_1, val_2), number_of_carry(val_1, val_2))
    #feature = (max_digit(val_1,val_2), digit_diff(val_1, val_2), number_of_carry(val_1, val_2))

    feature = (tot_digits, dif_digits, num_carry, num_zero, trail)
    #feature = (num_1_digit, num_2_digit, num_carry, num_zero)

    return feature

def max_digit (x, y) :
    if number_of_digit(x) >= number_of_digit(y) :
        return number_of_digit(x)
    return number_of_digit(y)

def number_of_digit (x) :
    return len(str(x))

def total_number_digit (x , y):
    return number_of_digit(x) + number_of_digit(y)

def digit_diff (x, y):
    return abs(number_of_digit(x) - number_of_digit(y))

def is_same_number (x, y) :
    if (x == y) :
        return True
    return False

def number_of_carry (x , y) :
  ctr = 0
  if(x == 0 and y == 0):
    return 0
  z = 0  
  for i in reversed(range(10)):
      z = x%10 + y%10 + z
      if z > 9:
        z = 1
      else:
        z = 0
      ctr += z
      x //= 10
      y //= 10
      
  return ctr

def number_of_zero (x , y) :
    def count_zeros(x):
        return str(x).count('0')
    return count_zeros(x) +count_zeros(y)

def non_trailing_zero_count(val_1, val_2):

    total_zero_1 = str(val_1).count('0')
    total_zero_2 = str(val_2).count('0')

    num1_str = str(val_1)
    num2_str = str(val_2)

    trail_1 = len(num1_str) - len(num1_str.rstrip('0'))
    trail_2 = len(num2_str) - len(num2_str.rstrip('0'))

    return ((len(num1_str) - trail_1) == 1  and  (len(num2_str) - trail_2) == 1  and val_1 != 0 and val_2 != 0 and total_zero_1 != 0 and total_zero_2 != 0)


    
def main ():
    MAX_NUM = 999
    bins = defaultdict(lambda: [])

    for num_1 in range(0, MAX_NUM + 1):
        for num_2 in range(0, MAX_NUM + 1):

            key = feature_extractor(num_1, num_2)
            #print("Problem: " + str(num_1) + " + " + str(num_2) + " = ? is mapped to feature space as: " + str(key) )

            bins[key].append((num_1, num_2))

    # Bin statistics
    print("Number of Bin: ", len(bins))
    x = list()
    for key in bins:
        print("Bin Name: " + str(key) + "   Bin Count: " + str(len(bins[key])))
        x.append(len(bins[key]))
        print(bins[key][0:100])
        print("")
    #plt.plot(x)
    #plt.ylabel('some numbers')
    #plt.show()

main()
