import Initializations
import EncryptionKeyGeneration
import random

def addPadding(data):
    
    paddedData = '' + data

    if(len(data) % 16 != 0):
        for i in range(0, 16 - (len(data) % 16)):
            paddedData += ' '

    return paddedData

def getEBCDICEquivalent(data, charTable):
    
    ebcdicEquivalent = []
    for i in range(0, len(data)):
        ebcdicEquivalent.append(charTable[data[i]])

    return ebcdicEquivalent

def getTextMatrix(data, charTable, columns):
    
    paddedData = addPadding(data)
    ebcdicEquivalentData = getEBCDICEquivalent(paddedData, charTable)

    textMatrix = []
    for i in range(0, len(ebcdicEquivalentData), columns):
        currentRow = []
        for j in range(i, i + columns):
            currentRow.append(ebcdicEquivalentData[j])
        textMatrix.append(currentRow)
    
    return textMatrix

def getSubtractiveMatrix(textMatrix, keyMatrix, blockSize):

    subtractiveMatrix = []
    for i in range(0, len(textMatrix), 4):
        constituentMatrices = []
        for j in range(i, i + 4):
            currentBlock = []
            for k in range(0, blockSize):
                currentBlock.append(textMatrix[j][k] - keyMatrix[j%4][k])
            constituentMatrices.append(currentBlock)
        subtractiveMatrix.extend(constituentMatrices)
    
    return subtractiveMatrix

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

def decimalToHex(dataList):
    hexData = ''
    for i in range(0, len(dataList)):
        hexData = hexData + "{:02x}".format(dataList[i])
    hexData = hexData.upper()
    return hexData

def encrypt(plainText):

    blockSize = 4
    charTable = Initializations.initializeTables()
    
    key = EncryptionKeyGeneration.generateKey(charTable)
    keyMatrix = EncryptionKeyGeneration.getKeyMatrix(key, charTable, blockSize)
    
    textMatrix = getTextMatrix(plainText, charTable, blockSize)
    subtractiveMatrix = getSubtractiveMatrix(textMatrix, keyMatrix, blockSize)

    linearData = []
    for i in range(0, len(subtractiveMatrix)):
        for j in range(0, blockSize):
            linearData.append(subtractiveMatrix[i][j])

    segment1 = linearData[:len(linearData)//2]
    segment2 = linearData[len(linearData)//2:]

    crossover(segment1, segment2)
    mutation(segment1, segment2)
    
    segment = segment1 + segment2

    finalCipher = decimalToHex(segment)
    key = key + str(blockSize) + 'CM'
    
    return finalCipher, key
