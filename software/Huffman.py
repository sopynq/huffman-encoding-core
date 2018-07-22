import time
import copy
from PIL import Image
import numpy as np
import Symbol as sb
import HuffmanDecode as hfd

class Node():
    def __init__(self,value=0,frequency=0):
        self.value=value
        self.frequency=frequency
        self.left=None
        self.right=None
        self.Isremoved=False
    def incdepth(self):
        self.depth=self.depth+1

def readimage(path):
    im=Image.open(path)
    [imr,img,imb]=im.split()
    (width,height)=imr.size
    imr_dat = imr.getdata()
    imr_dat = np.matrix(imr_dat, dtype='int')
    img_dat = img.getdata()
    img_dat = np.matrix(img_dat, dtype='int')
    imb_dat = imb.getdata()
    imb_dat = np.matrix(imb_dat, dtype='int')
    im_total=np.column_stack((imr_dat,img_dat))
    im_total = np.column_stack((im_total, imb_dat))
    im_total=(im_total.tolist())
    (dict,dict_depth,sy)=huffman(im_total[0])
    strr=hfd.generateString(im_total[0],dict_depth,sy)
    decoded=hfd.HuffmanDecode(strr,sy,dict_depth)
    right=True
    for i in range(len(decoded)):
        if decoded[i]!=im_total[0][i]:
            print("error!\torigin=",end='\t')
            print(im_total[0][i],end='\t')
            print("error!\tdeocded",end='\t')
            print(decoded[i],end='\n')
            right=False
    if right==True:
        for i in range(len(decoded)):
            print(decoded[i],end='\t')
            if i % 4==0:
                print()

def huffman(str):
    #print(len(str))
    value=[];
    frequency=[];
    nodes=[]
    for i in range(len(str)):
        textin=str[i]
        judge = textin in value
        if judge == False:
            value.append(textin)
            frequency.append(1)
        else:
            ind=value.index(textin)
            frequency[ind]=frequency[ind]+1

    for i in range(len(value)):
        nodes.append(Node(value[i], frequency[i]))




    # 统计
    time_start = time.time()

    #范式霍夫曼编码，开始
    (ret1_sy, ret1_dep, ret1_fre, ret2_sy, ret2_dep, ret2_fre)=Huffman_Create(nodes)

    time_end = time.time()

    his=truncateTree(ret2_sy, ret2_dep)
    res=createCodeWord(his, ret2_dep, ret2_sy)

    print('totally cost', time_end - time_start)
    for i in range(len(ret1_sy)):
        print("symbol=",end='\t')
        print(ret2_sy[i], end='\t')
        print("depth=", end='\t')
        print(ret2_dep[i], end='\n')
    print("====================================================")
    for i in range(len(res)):
        print("symbol=",end='\t')
        print(ret2_sy[i], end='\t')
        print("code=", end='\t')
        print(res[i], end='\n')

    return (res,ret2_dep,ret2_sy)

def Huffman_Create(nodes):
#        for i in range(len(nodes)):
#            print("value=  ",end='\t')
#            print(nodes[i].value, end='\t')
#            print("frequency=  ", end='\t')
#            print(nodes[i].frequency, end='\n')


#        print("==========================================================")

        copy_nodes=copy.copy(nodes)
        while len(copy_nodes)>1:
            (ind1,ind2)=get2minInd(copy_nodes)
            larger=ind1
            smaller=ind2
#            print("smallest=",end='\t')
#            print(copy_nodes[ind1].frequency,end='\t')
#            print("smallest2",end='\t')
#            print(copy_nodes[ind2].frequency,end='\n')
            if ind1<ind2:
                larger=ind2
                smaller=ind1
            child1=copy.copy(copy_nodes[larger])
            child2 = copy.copy(copy_nodes[smaller])
            newnode=Node(frequency=copy_nodes[larger].frequency+copy_nodes[smaller].frequency,value=0)
            newnode.left=child1
            newnode.right=child2
            copy_nodes.remove(copy_nodes[larger])
            copy_nodes.remove(copy_nodes[smaller])
            copy_nodes.append(newnode)
        ##
        symbol_list=[]
        depth_list=[]
        freq_list=[]
        dfs(copy_nodes[0],0,symbol_list,depth_list,freq_list)

        ##
        #for i in range(len(symbol_list)):
        #    print(depth_list[i])

        for i in range(len(symbol_list)):
            for j in range(i+1,len(symbol_list)):
                if symbol_list[i]>symbol_list[j]:
                    temp_symbol = symbol_list[i]
                    temp_depth = depth_list[i]
                    temp_freq = freq_list[i]
                    symbol_list[i] = symbol_list[j]
                    depth_list[i] = depth_list[j]
                    freq_list[i] = freq_list[j]
                    symbol_list[j] = temp_symbol
                    depth_list[j] = temp_depth
                    freq_list[j] = temp_freq

        ret1_sy=copy.copy(symbol_list)
        ret1_dep=copy.copy(depth_list)
        ret1_fre=copy.copy(freq_list)

        for i in range(len(symbol_list)-1):
            for j in range(len(symbol_list)-1):
                if depth_list[j]>depth_list[j+1]:
                    temp_symbol = symbol_list[j]
                    temp_depth = depth_list[j]
                    temp_freq = freq_list[j]
                    symbol_list[j] = symbol_list[j+1]
                    depth_list[j] = depth_list[j+1]
                    freq_list[j] = freq_list[j+1]
                    symbol_list[j+1] = temp_symbol
                    depth_list[j+1] = temp_depth
                    freq_list[j+1] = temp_freq


        ret2_sy = copy.copy(symbol_list)
        ret2_dep = copy.copy(depth_list)
        ret2_fre = copy.copy(freq_list)

        return (ret1_sy,ret1_dep,ret1_fre,ret2_sy,ret2_dep,ret2_fre)

def dfs(node,depth,symbol_list,depth_list,freq_list):
#    print("frequency=",end='\t')
#    print(node.frequency,end='\t')
#    print("depth=",end='\t')
#    print(depth,end='\n')
    if node.left is None :
        symbol_list.append(node.value)
        depth_list.append(depth)
        freq_list.append(node.frequency)
        return
    else:
        dfs(node.right,depth+1,symbol_list,depth_list,freq_list)
        dfs(node.left,depth+1,symbol_list,depth_list,freq_list)

def get2minInd(nodes):
    minfreq = 999999999
    minindex1 = -1
    minfreq2 = 999999999
    minindex2 = -1
    for i in range(len(nodes)):
        freq=nodes[i].frequency
        if freq<minfreq:
            minindex1=i
            minfreq=freq

    for i in range(len(nodes)):
        freq=nodes[i].frequency
        if freq<minfreq2:
            if i != minindex1:
                minindex2=i
                minfreq2=freq

    return (minindex1,minindex2)

def truncateTree(symbols,depth):
    Historalgram=[]
    Historalgram.append(0)
    for i in range(depth[-1]):
        Historalgram.append(0)
    for i in range(len(depth)):
        Historalgram[depth[i]]=Historalgram[depth[i]]+1

    outhis=copy.copy(Historalgram)

    j=30
    for i in range(depth[-1]-1,-1,30):
        while outhis[i]!=0:
            if j==30:
                j=j-1
                while outhis==0:
                    j=j-1
            outhis[j]-=1
            outhis[j+1] += 2
            outhis[i-1] += 1
            outhis[i] -= 2
            j+=1

    return outhis

def createCodeWord(histogram,depth,symbols):
    codeword=[]
    codeword.append(0)
    for i in range(1,len(depth)):
        if depth[i]==depth[i-1]:
            codeword.append(codeword[i-1]+1)
        else:
            codeword.append((codeword[i-1]+1)<<(depth[i]-depth[i-1]))
    return codeword
