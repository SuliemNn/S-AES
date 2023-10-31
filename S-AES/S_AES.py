# 所有的二进制都用字符串进行运算

import time

#轮常数
cons1="10000000"
cons2="00110000"

# 置换盒
S_Box = [['9', '4', 'A', 'B'],
         ['D', '1', '8', '5'],
         ['6', '2', '0', '3'],
         ['C', 'E', 'F', '7']]
# 逆置换盒
S_deBox = [['A', '5', '9', 'B'],
           ['1', '7', '8', 'F'],
           ['6', '0', '2', '3'],
           ['C', '4', 'D', 'E']]

mixMatrix = [['1', '4'], ['4', '1']]
deMixMatrix = [['9', '2'], ['2', '9']]


# 输入二进制字符串，返回二进制对应的状态矩阵
def toStateMartix(bytetext):
    martix = [[bytetext[0:4], bytetext[8:12]],
              [bytetext[4:8], bytetext[12:16]]]
    return martix


# 输入二进制状态矩阵，返回对应的二进制字符串
def reStateMartix(martix):
    byteText = martix[0][0] + martix[1][0] + martix[0][1] + martix[1][1]
    return byteText


# 轮密钥加密：逐位进行异或操作 输入两个二进制字符串，输出结果=>二进制字符串
def xor(text1, text2):
    i = 0
    restext = ""
    while i < len(text1):
        if text1[i] == text2[i]:
            restext += "0"
        else:
            restext += "1"
        i += 1
    return restext


# 半字节替代，传入二进制字符串，返回二进制字符串
def halfByteReplace(text, Box):
    index = 0
    result = ""
    while index < len(text):
        i = int(text[index:index + 2], 2)
        j = int(text[index + 2:index + 4], 2)
        result += Box[i][j]
        index += 4

    # 十六进制转换二进制
    result = bin(int(result, 16))[2:].zfill(16)
    return result


# 左循环移位，传入二进制字符串，返回二进制字符串
def left_shift(text):
    stateMartix = toStateMartix(text)

    # 交换
    tem = stateMartix[1][0]
    stateMartix[1][0] = stateMartix[1][1]
    stateMartix[1][1] = tem

    return reStateMartix(stateMartix)


def gf_add(a, b):
    return a ^ b  # 二进制数的异或运算即为GF(2^4)的加法运算


def gf_multiply(a, b):
    result = 0
    while b != 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x10:
            a ^= 0b10011  # GF(2^4)的乘法多项式 x^4 + x + 1
        b >>= 1
    return result % 16  # 结果需要模上16，因为GF(2^4)的元素是4位二进制数


# 列混淆函数，传入一个列混淆矩阵和一个二进制字符串。返回一个二进制字符串
def colMix(colMartix, byteText):
    myMartix = toStateMartix(byteText)
    resMartix = [["", ""], ["", ""]]
    resMartix[0][0] = bin(gf_add(gf_multiply(int(colMartix[0][0], 16), int(myMartix[0][0], 2)),
                                 gf_multiply(int(colMartix[0][1], 16), int(myMartix[1][0], 2))))[2:].zfill(4)

    resMartix[0][1] = bin(gf_add(gf_multiply(int(colMartix[0][0], 16), int(myMartix[0][1], 2)),
                                 gf_multiply(int(colMartix[0][1], 16), int(myMartix[1][1], 2))))[2:].zfill(4)

    resMartix[1][0] = bin(gf_add(gf_multiply(int(colMartix[1][0], 16), int(myMartix[0][0], 2)),
                                 gf_multiply(int(colMartix[1][1], 16), int(myMartix[1][0], 2))))[2:].zfill(4)

    resMartix[1][1] = bin(gf_add(gf_multiply(int(colMartix[1][0], 16), int(myMartix[0][1], 2)),
                                 gf_multiply(int(colMartix[1][1], 16), int(myMartix[1][1], 2))))[2:].zfill(4)

    return reStateMartix(resMartix)


#密钥扩展的g函数，
def G(byteText,cons,Box):
    #第一步进行左循环移位，将左右两个进行互换
    resText=byteText[4:]+byteText[0:4]

    #第二步进行S盒替代
    index = 0
    result = ""
    while index < len(resText):
        i = int(resText[index:index + 2], 2)
        j = int(resText[index + 2:index + 4], 2)
        result += Box[i][j]
        index += 4

    # 十六进制转换二进制
    result = bin(int(result, 16))[2:].zfill(8)

    #第三步，与轮常数进行异或
    result=xor(result,cons)

    return result


#输入初始密钥，输出扩展之后的密钥
def expandKey(key,cons,Box):
    rightKey = key[8:]
    leftKey = key[0:8]

    # 左边的密钥由右半部分g(i-1)与左半部分异或得到
    resLeft=xor(G(rightKey,cons,Box),leftKey)

    # 第i个密钥的右半部分由第i个密钥的左半部分与第i-1个密钥的右半部分进行异或得到
    resRight=xor(resLeft,rightKey)
    return resLeft+resRight

def enCrypt(plainText, key):

    plainText=bin(int(plainText,2))[2:].zfill(16)
    key = bin(int(key, 2))[2:].zfill(16)


    #进行密钥扩展
    keyList=[key, expandKey(key, cons1, S_Box), expandKey(expandKey(key, cons1, S_Box), cons2, S_Box)]

    #第0轮加密：将明文与初始密文进行异或
    temText=xor(plainText, keyList[0])

    #第1轮加密

    #1.1 半字节代替：对temText进行半字节替代
    temText=halfByteReplace(temText,S_Box)

    #1.2 行位移
    temText=left_shift(temText)

    #1.3 列混淆
    temText=colMix(mixMatrix,temText)

    #1.3 轮密钥加密
    temText=xor(temText, keyList[1])


    #第2轮加密

    #2.1 半字节替代
    temText=halfByteReplace(temText,S_Box)

    #2.2 行位移
    temText=left_shift(temText)

    #2.3 轮密钥加
    temText=xor(temText, keyList[2])

    return temText

def deCrypt(cyberText,key):

    cyberText=bin(int(cyberText,2))[2:].zfill(16)
    key = bin(int(key, 2))[2:].zfill(16)

    #将key进行扩展
    keyList = [key, expandKey(key, cons1, S_Box), expandKey(expandKey(key, cons1, S_Box), cons2, S_Box)]

    # 第0轮解密
    # 密钥加
    temText=xor(cyberText,keyList[2])

    #第一轮解密

    #1.1 逆行移位
    temText=left_shift(temText)

    #1.2 逆半字节替代
    temText=halfByteReplace(temText,S_deBox)

    #1.3 轮密钥加
    temText=xor(temText,keyList[1])

    #1.4 逆列混淆
    temText=colMix(deMixMatrix,temText)


    #第二轮解密

    #2.1 逆行移位
    temText=left_shift(temText)

    # 2.2 逆半字节替代
    temText=halfByteReplace(temText,S_deBox)


    # 2.3 轮密钥加
    temText=xor(temText,keyList[0])

    return temText

# ascii 编码的实现:传入一个字符串和密钥，返回密文数组
def asciiEnCrypt(str,key):
    #把一个str转换为ascList
    ascList=[]
    for i in str:
        ascList.append(ord(i))

    cyberList=[]
    for i in ascList:
        tem=bin(i)[2:]
        cyberList.append(enCrypt(tem,key))
    return cyberList

#传入一个cyberList，返回对应的字符串数组
def asciiDeCrypt(cyberList,key):
    ascList=[]
    for i in cyberList:
        ascList.append(int(deCrypt(i,key),2))

    strLst=[]
    for i in ascList:
        strLst.append(chr(i))
    return lstToStr(strLst)

#把字符串数组转换为字符串
def lstToStr(lst):
    str=""
    for i in lst:
        str+=i
    return str

#多重加密
def multiplyEnCrypt(plainText,key):
    level=len(key)/16
    count=0
    cyberText=plainText
    while count<level:
        temkey=key[0:16]
        key=key[16:]
        cyberText=enCrypt(cyberText,temkey)
        count+=1
    return cyberText

#多重解密
def multiplyDeCrypt(cyberText,key):
    level = len(key) / 16
    count=0
    plainText=cyberText
    while count<level:
        temkey=key[-16:]
        key=key[0:-16]
        plainText=deCrypt(plainText,temkey)
        count+=1
    return plainText

#暴力破解函数,输入明文和密文，返回其对应的key数组
def breakOut(plainText,cyberText):
    start_time=time.time()
    key=0
    keyLst=[]
    while key<2**16-1:
        myCyber=enCrypt(plainText,bin(key)[2:])
        if myCyber == cyberText:
            keyLst.append(key)
        key+=1
    newkey=[]
    for i in keyLst:
        newkey.append(bin(i)[2:])
    return newkey,time.time()-start_time

if __name__ == '__main__':
    # 置换盒测试程序
    plainText = bin(int("8A1C", 16))[2:]
    print("置换盒测试")
    print(plainText)
    print(hex(int(halfByteReplace(plainText, S_Box), 2)))
    print(hex(int(halfByteReplace(halfByteReplace(plainText, S_Box), S_deBox), 2)))

    # 行移位测试程序
    print("行移位测试")
    resText = halfByteReplace(plainText, S_Box)
    print(hex(int(left_shift(resText), 2)))


    #列混淆函数确认
    print("列混淆函数确认")
    resText=left_shift(resText)
    resText2 = colMix(mixMatrix,resText)
    print(hex(int(resText2,2)))
    resText3 = colMix(deMixMatrix,resText2)
    print(hex(int(resText3,2)))

    #密钥扩展确认
    cyberText="1010011100111011"
    print("密钥扩展确认")
    print("第一轮加密："+expandKey(cyberText,cons1,S_Box))
    print("第二轮加密：" + expandKey(expandKey(cyberText,cons1,S_Box), cons2, S_Box))

    #加密确认
    #1101111000001101
    print("加密确认")
    print("明文为：0110111101101011")
    print("密文为：" + enCrypt(plainText="0110111101101011", key="1010011100111011"))
    testcyber=enCrypt(plainText="1100110000110011", key="1010011100111011")
    #mystr="0000 0111 0011 1000"
    print("解密："+deCrypt(testcyber,key="1010011100111011"))


    #ascii扩展
    print("ascii扩展")
    str="Hello world!!!"
    cyberlst=asciiEnCrypt(str, key="1010011100111011")
    print(cyberlst)
    print(asciiDeCrypt(cyberlst,key="1010011100111011"))


    #多重加密
    print("多重加密")
    mulcyber=multiplyEnCrypt("0110111101101011","10100111001110110110111101101011")
    print("加密后的密文为："+mulcyber)
    print("解密后的明文为："+multiplyDeCrypt(mulcyber,"10100111001110110110111101101011"))

    #暴力破解
    print("暴力破解")
    print(breakOut("0110111101101011","0000011100111000"))






