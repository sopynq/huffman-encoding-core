import copy


def generateString(str, dict_depth, dict_sy):
    codeword = bitReconstruction(dict_sy, dict_depth)
    stringFin = []
    for i in range(len(str)):
        index_sy = dict_sy.index(str[i])
        codenum = codeword[index_sy]
        strcode = bin(codenum,dict_depth[index_sy])
        for j in range(len(strcode)):
            stringFin.append(strcode[j])
    return stringFin


def bin(num,width):
    ap = copy.copy(num)
    strret = []
    ss=True
    if ss==False:
        strret.append('0')
    else:
        for i in range(width):
            it = ap % 2
            # print(it)
            ap = int(ap / 2)
            if it == 0:
                strret.append('0')
            else:
                if it == 1:
                    strret.append('1')
                else:
                    print("error ")
        left = 0
        right = len(strret) - 1
        while left <= right:
            temp = strret[left]
            strret[left] = strret[right]
            strret[right] = temp
            left += 1
            right -= 1
    return strret


def HuffmanDecode(str, dict_sy, dict_depth):
    deocded = []
    # str char 0 , 1 , 0 , 0
    wordInDetection = 0
    widthInDetection = 0

    codeword = bitReconstruction(dict_sy, dict_depth)
    (maxValue, maxIndex) = FindMaxCodeWord(codeword, dict_depth)

    for i in range(len(str)):
        bit = 0
        if str[i] == '1':
            bit = 1
        wordInDetection=wordInDetection << 1
        wordInDetection += bit
        widthInDetection += 1
        maxval = maxValue[widthInDetection]
        maxind = maxIndex[widthInDetection]

        if maxval >= wordInDetection:
            # get new decoded bit
            desymbol = dict_sy[(maxind - (maxval - wordInDetection))]
            deocded.append(desymbol)
            # 复原
            wordInDetection = 0
            widthInDetection = 0
    return deocded


def bitReconstruction(dict_sy, dict_depth):
    codeword = []
    codeword.append(0)
    for i in range(1, len(dict_depth)):
        if dict_depth[i] == dict_depth[i - 1]:
            codeword.append(codeword[i - 1] + 1)
        else:
            codeword.append((codeword[i - 1] + 1) << (dict_depth[i] - dict_depth[i - 1]))
    for i in range(len(codeword)):
        print("symbol",end='\t')
        print(dict_sy[i],end='\t')
        print("codeword=",end='\t')
        print(codeword[i],end='\n')
    print("*******************************************************")
    return codeword


def FindMaxCodeWord(codeword, depth):
    maxValue = []
    maxIndex = []
    origin_depth = depth[0]
    for i in range(origin_depth):
        maxValue.append(-1)
        maxIndex.append(-1)

    # 每个depth 对应的最大值和最大值所在的下标
    for i in range(1, len(depth)):
        if depth[i] == depth[i - 1]:
            continue
        else:
            maxValue.append(codeword[i-1])
            maxIndex.append(i-1)
            for j in range((depth[i] - depth[i - 1] - 1)):
                maxValue.append(-1)
                maxIndex.append(-1)
    maxValue.append(codeword[len(depth)-1])
    maxIndex.append(len(depth)-1)

    return (maxValue, maxIndex)
