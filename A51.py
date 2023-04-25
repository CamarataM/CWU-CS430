
regX = []
regY = []
regZ = []

lenX = 19
lenY = 22
lenZ = 23

#Populating each register
def fillRegisters(key):

    i = 0

    while (i < lenX):
        regX.insert(i, key[i])
        i += 1

    j = lenX

    while (j < lenX + lenY):
        regY.insert(j - lenX, key[j])
        j += 1

    k = lenX + lenY

    while (k < lenX + lenY + lenZ):
        regZ.insert(k - lenX - lenY, key[k])
        k += 1

def getMajority(x,y,z):

    if (x+y+z > 1):
        return 1
    else:
        return 0

#Generate the keystream for the key
def getKeyStream():
    #Generating keystream using A5/1 algorithm
    keyStream = []

    while(len(keyStream) != 32):

        majority = getMajority(int(regX[-1]), int(regY[-1]), int(regZ[-1]))
        
        #Check if shift registers match majority
        #If any of the registers equal the majority, step the register.
        if (int(regX[-1]) == majority):
            t = int(regX[13]) ^ int(regX[16]) ^ int(regX[17]) ^ int(regX[18])
            regX.pop()
            regX.insert(0, t)
        
        if (int(regY[-1]) == majority):
            t = int(regY[20]) ^ int(regY[21])
            regY.pop()
            regY.insert(0, t)
        
        if (int(regZ[-1]) == majority):
            t = int(regZ[7]) ^ int(regZ[20]) ^ int(regZ[21]) ^ int(regZ[22])
            regZ.pop()
            regZ.insert(0, t)
        
        key = int(regX[18]) ^ int(regY[21]) ^ int(regZ[22])
        keyStream.append(key)
        
    print("32 Keystream bits:", keyStream)
    print("\nFinal Contents of Registers: ")
    print("X:", regX)
    print("Y:", regY)
    print("Z:", regZ)     



def main():
    key = "1010101010101010101110011001100110011001111100001111000011110000"

    fillRegisters(key)
    getKeyStream()


main()
