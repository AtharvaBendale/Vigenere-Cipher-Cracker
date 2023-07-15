list_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Defining all necessary functions

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
    count = [0 for i in range(26)]
    for letter in ciphertext:
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
for j in range(2, 100):
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

key_lengths = []
for i in sorted_ics[:10]:
    key_lengths.append(avg_ics.index(i))
key_lengths = min(key_lengths)

# Expected probabilities of all alphabets in standard dictionary distribution
expected_probs = [0.078, 0.02, 0.04, 0.038, 0.11, 0.014, 0.03, 0.023, 0.086, 0.0021, 0.0097, 0.053, 0.027, 0.072, 0.061, 0.028, 0.0019, 0.073, 0.087, 0.067, 0.033, 0.01, 0.0091, 0.0027, 0.016, 0.0044]

# Determining the keyword
possible_list = [[] for __ in range(key_lengths)]
keyword = ""

for i in range(key_lengths):
    text = ciphertext[i::key_lengths]
    for _ in range(26):
        text = step(text)
        prob = probs(text)
        possible_list[i].append(prob)
    keyword += list_letter[::-1][possible_list[i].index(min(possible_list[i]))]


print("Plaintext:")
print(decrypt(inputtext, keyword))
print(f"\nKey: {keyword}")