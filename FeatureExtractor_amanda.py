
from collections import defaultdict
import matplotlib.pyplot as plt

# For two , four digit numbers, there are a total of (10,0000)^2 permutations of problems
#Start Small and progressively increase the maxnum

# digit 
# number of 0 
# caret 



def feature_extractor(val_1, val_2):

    #feature = (total_number_digit(val_1, val_2), digit_diff(val_1, val_2), is_same_number(val_1, val_2), number_of_carry(val_1, val_2), number_of_zero(val_1, val_2))
    #feature = (number_of_digit(val_1),number_of_digit(val_2), is_same_number(val_1, val_2), number_of_carry(val_1, val_2), number_of_zero(val_1, val_2))
    
    feature = (total_number_digit(val_1, val_2), digit_diff(val_1, val_2), number_of_carry(val_1, val_2))
    #feature = (max_digit(val_1,val_2), digit_diff(val_1, val_2), number_of_carry(val_1, val_2))
    
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
    
    
def main ():
    MAX_NUM = 5000
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
        #print(bins[key])
        print("")
    # plt.plot(x)
    # plt.ylabel('some numbers')
    # plt.show()

main()
