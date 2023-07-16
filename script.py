import math
import argparse

list_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# Defining all necessary functions

parser = argparse.ArgumentParser(description='Vigenere Cipher Cracker')
parser.add_argument('-r', '--redo', required=False, type=int,help="'1' if you are not satisfied with the initial ouptput of decrypted text.")
args = parser.parse_args()
redo = bool(args.redo)

def decrypt(text, keyword):
    output = ""
    i = 0
    for char in text:
        if char.lower() not in list_letter:
            output = output + char
        else:
            if char.islower():
                output = output + list_letter[(list_letter.index(char) - list_letter.index(keyword[i%len(keyword)]))%26]
            else:
                char = char.lower()
                output = output + list_letter[(list_letter.index(char) - list_letter.index(keyword[i%len(keyword)]))%26].upper()
            i += 1
    return output

def IC(ciphertext):
    # print(ciphertext)
    count = [0 for i in range(26)]
    for letter in ciphertext:
        if letter not in list_letter:
            print(f"'{letter}' is not a valid input character.")
            exit()
        count[list_letter.index(letter)] += 1
    count = [count[i]*(count[i]-1) for i in range(len(count))]
    ic = sum(count)/(len(ciphertext)*(len(ciphertext)-1))
    return ic

def step(text):
    for i in range(len(text)):
        index = list_letter.index(text[i])
    text = [list_letter[(list_letter.index(letter)+1)%26] for letter in text]
    text = "".join(text)
    return text

def probs(text):
    # print(text)
    text = [text[i] for i in range(len(text))]
    # print(text)
    prob = []
    for i in range(26):
        prob.append(text.count(list_letter[i]))
    length = len(text)
    prob = [(prob[i]-expected_probs[i]*length)**2/(expected_probs[i]*length) for i in range(26)]
    prob = sum(prob)
    return prob

def filter_key(key_list, limit):
    count = [0 for _ in range(1, limit+1)]
    for i in range(len(key_list)):
        for j in range(i+1, len(key_list)):
            count[math.gcd(key_list[i], key_list[j])-1] = count[math.gcd(key_list[i], key_list[j])-1] + 1
    print(count)
    sorted_list = [count[_] for _ in range(len(count))]
    sorted_list.sort(reverse=True)
    count = [count.index(sorted_list[j])+1 for j in range(len(count))]
    return count

# Taking the input ciphertext
inputtext = input()

# Preprocessing the input text
ciphertext = inputtext.lower()
symbols = "!@#$%^&*()_+=-} {[]|\:;'\"<>,.?/~`"

for symbol in symbols:
    ciphertext = ciphertext.replace(symbol, "")

for i in range(10):
    ciphertext = ciphertext.replace(str(i), "")

# Calculating the average TC values for all possible key length
avg_ics = [0, 0]
for j in range(2, len(ciphertext)//2):
    sum_ic = 0
    for i in range(j):
        text = ciphertext[i::j]
        ic = IC(text)
        sum_ic += ic
    sum_ic /= j
    avg_ics.append(sum_ic)

# Determining the key length
sorted_ics = [i for i in avg_ics]
sorted_ics.sort(reverse=True)

key_length_list = []
for i in sorted_ics[:10]:
    key_length_list.append(avg_ics.index(i))

# Finding the most appropriate key
key_lengths = filter_key(key_length_list, max(key_length_list))

# Expected probabilities of all alphabets in standard dictionary distribution
expected_probs = [0.078, 0.02, 0.04, 0.038, 0.11, 0.014, 0.03, 0.023, 0.086, 0.0021, 0.0097, 0.053, 0.027, 0.072, 0.061, 0.028, 0.0019, 0.073, 0.087, 0.067, 0.033, 0.01, 0.0091, 0.0027, 0.016, 0.0044]

# Determining the keyword
for i, key_length in enumerate(key_lengths):
    possible_list = [[] for __ in range(key_length)]
    keyword = ""

    for i in range(key_length):
        text = ciphertext[i::key_length]
        for _ in range(26):
            text = step(text)
            prob = probs(text)
            possible_list[i].append(prob)
        keyword += list_letter[::-1][possible_list[i].index(min(possible_list[i]))]

    print("Plaintext:")
    print(decrypt(inputtext, keyword))
    print(f"\nKey: {keyword}")

    if redo:
        satisfied = input("\nAre you satisfied with the decryption (Y/n) : ")
        if satisfied == 'Y':
            break
        else:
            print("\n")
    else:
        break
