def getEBCDICEquivalent(data, charTable):
    ebcdicEquivalent = []
    for i in range(0, len(data)):
        ebcdicEquivalent.append(charTable[data[i]])
    return ebcdicEquivalent

def rightShiftByTwo(dataList):
    rightShiftedData = []
    for i in range(0, len(dataList)):
        rightShiftedData.append(dataList[i] >> 2)
    return rightShiftedData

def getKeyMatrix(key, charTable, columns):
    ebcdicEquivalent = getEBCDICEquivalent(key, charTable)
    rightShiftedEBCDICEquivalent = rightShiftByTwo(ebcdicEquivalent)

    keyMatrix = []
    for i in range(0, len(rightShiftedEBCDICEquivalent), columns):
        currentRow = []
        for j in range(i, i + columns):
            currentRow.append(rightShiftedEBCDICEquivalent[j])
        keyMatrix.append(currentRow)
    
    return keyMatrix
