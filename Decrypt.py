import Initializations
import DecryptionKeyGeneration
import random

def getPlainText(textMatrix, charTable, columns):
    
    plainText = ''
    characters = charTable.keys()
    for i in range(0, len(textMatrix)):
        currentRow = textMatrix[i]
        for j in range(0, len(currentRow)):
            for k in characters:
                if(charTable[k] == currentRow[j]):
                    plainText += k
                    break
                    
    plainText = plainText.rstrip()
    return plainText

def getTextMatrix(subtractiveMatrix, keyMatrix, blockSize):

    textMatrix = []
    for i in range(0, len(subtractiveMatrix), 4):
        constituentMatrices = []
        for j in range(i, i + 4):
            currentBlock = []
            for k in range(0, blockSize):
                currentBlock.append(subtractiveMatrix[j][k] + keyMatrix[j%4][k])
            constituentMatrices.append(currentBlock)
        textMatrix.extend(constituentMatrices)
    
    return textMatrix

def crossover(segment1, segment2):

    for i in range(0, len(segment1)):
        if(i%2 == 1):
            segment1[i], segment2[i] = segment2[i], segment1[i]

    return

def mutation(segment1, segment2):

    for i in range(0, len(segment1)):
        bits1 = []
        bits2 = []
        for j in range(7, -1, -1):
            bits1.append((segment1[i] >> j) & 1)
            bits2.append((segment2[i] >> j) & 1)
        bits1[2], bits1[5] = bits1[5], bits1[2]
        bits1[3], bits1[4] = bits1[4], bits1[3]
        bits2[2], bits2[5] = bits2[5], bits2[2]
        bits2[3], bits2[4] = bits2[4], bits2[3]
        value1 = 0
        value2 = 0
        for j in range(7, -1, -1):
            value1 = value1 + bits1[7-j] * (2 ** j)
            value2 = value2 + bits2[7-j] * (2 ** j)
        segment1[i] = value1
        segment2[i] = value2
    
    return

def hexToDecimal(dataList):
    decimalData = []
    for i in range(0, len(dataList)):
        decimalData.append(int(dataList[i], 16))
    return decimalData

def decrypt(cipherText, key):

    blockSize = int(key[-3])
    key = key[:16]

    charTable = Initializations.initializeTables()
    
    keyMatrix = DecryptionKeyGeneration.getKeyMatrix(key, charTable, blockSize)

    cipherText = [cipherText[i: i+2] for i in range(0, len(cipherText), 2)]

    segment = hexToDecimal(cipherText)

    segment1 = segment[:len(segment)//2]
    segment2 = segment[len(segment)//2:]

    mutation(segment1, segment2)
    crossover(segment1, segment2)

    linearData = segment1 + segment2

    subtractiveMatrix = []
    for i in range(0, len(linearData), blockSize):
        currentBlock = []
        for j in range(i, i + blockSize):
            currentBlock.append(linearData[j])
        subtractiveMatrix.append(currentBlock)

    textMatrix = getTextMatrix(subtractiveMatrix, keyMatrix, blockSize)

    plainText = getPlainText(textMatrix, charTable, blockSize)
    
    return plainText
