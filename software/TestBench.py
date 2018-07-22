import Huffman as hf
import HuffmanDecode as hfd




teststr=[1,1,1,1,1,1,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5]
(dict, dict_depth, sy) = hf.huffman(teststr)
strr = hfd.generateString(teststr, dict_depth, sy)
decoded = hfd.HuffmanDecode(strr, sy, dict_depth)
right=True
for i in range(len(decoded)):
    if decoded[i] != teststr[i]:
        print("error!\torigin=", end='\t')
        print(teststr[i], end='\t')
        print("error!\tdeocded", end='\t')
        print(decoded[i], end='\n')
        right=False

if right==True:
    for i in range(len(decoded)):
        print(decoded[i],end='\t')
        if i % 5==0:
            print()
