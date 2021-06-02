from FeatureExtractor import feature_extractor

def student1(x, y):
    features = feature_extractor(x, y)
    num1_digits = features[0]
    num2_digits = features[1]
    num_carry = features[2]

    reward = 10 * max(num1_digits, num2_digits) + num_carry * 10

    if max(num1_digits, num2_digits) == 3:
        return -reward
    return reward
