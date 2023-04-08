import string
from collections import Counter

# Check if the given key is valid by sorting it and comparing it with the English alphabet.
def isValidKey(key):
    if len(key) != 26:
        print("Error: length of key must be equal to 26!")
        return False
    
    sortedKey = ''.join(sorted(list(key)))
    
    if sortedKey != string.ascii_lowercase:
        print("Error: key must contain all letters of the English alphabet exactly once.")
        return False
    
    return True

# Decrypts a message given the key and cipher text
def decryptText(key, cipherText):
    message = ''
    
    #For each letter in the cipher text, retrieve its index from the key and append the corresponding Letter from alphabet[index]
    #...to the decrypted message.
    for letter in cipherText:
        #Checking if the letter lowercase or uppercase
        if letter.lower() in string.ascii_lowercase:

            index = string.ascii_lowercase.index(letter.lower())

            if letter.islower():
                message += key[index]
            else:
                message += key[index].upper()
        else:
            message += letter

    return message

# Prompt user for ciphertext
cipherText = input("Enter Ciphertext: ")
cipherText = cipherText.lower()

charFrequencies = Counter(cipherText)

print("The character counts are: ")
print(charFrequencies)



key = input("Enter a possible key: ")
key = key.lower()

while isValidKey(key) == False:
    key = input("Enter a possible key: ")

decryptedText = decryptText(key, cipherText)

print("The decrypted message is: " + decryptedText)

