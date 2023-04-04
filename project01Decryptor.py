from collections import Counter

alphabet = "abcdefghijklmnopqrstuvwxyz"

#Check if the given key is valid by sorting it and comparing it with the English alphabet.
def isValidKey(key):
    if len(key) != 26:
        print("Error: length of key must be equal to 26!")
        return False
    
    sortedKey = ''.join(sorted(list(key)))
    
    if(sortedKey != alphabet):
        print("Error: key must only contain letters of the English alphabet (having no duplicates).")
        return False
    
    return True

#Decrypts a messsage given the key and cipher text.
def decryptText(key, cipherText):
    message = ''
    
    #For each letter in the cipher text, retrieve its index from the key and append the corresponding Letter from alphabet[index]
    #...to the decrypted message.
    for letter in cipherText:
        index = key.find(letter)
        message += alphabet[index]

    return message


cipherText = input("Enter Ciphertext: ")

cipherText = cipherText.lower()

charFrequencies = Counter(cipherText)

print("The character counts are: ")
print(charFrequencies)

key = input("Enter a possible key: ")

key = key.lower()

while isValidKey(key) == False:
    key = input("Enter a possible key: ")


print("The decrypted message is: " + decryptText(key, cipherText))



