# S-AES
文件说明：
pycharm打开主文件夹：
index.py文件为启动文件，在当前文件页面启动即可。
S_AES.py文件为算法实现文件
templates为前端页面文件夹
static为前端所用的js和css文件夹

## 1. 基本测试

对照实验资料进行基础测试操作，按部就班

```python
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
```

``` python
置换盒测试
1000101000011100
0x604c
0x8a1c
行移位测试
0x6c40
列混淆函数确认
0x3743
0x6c40
密钥扩展确认
第一轮加密：0001110000100111
第二轮加密：0111011001010001
加密确认
明文为：0110111101101011
密文为：0000011100111000
解密：1100110000110011
ascii扩展
['0100011111000100', '0001111010001010', '1111111010000011', '1111111010000011', '1110111010000101', '1001001000010110', '1010110100111000', '1110111010000101', '0101110100111110', '1111111010000011', '1000111010000010', '0011001000011101', '0011001000011101', '0011001000011101']
['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!', '!', '!']
多重加密
加密后的密文为：0101101111011000
解密后的明文为：0110111101101011
暴力破解
(['1010010001011111', '1010011100111011'], 2.1165568828582764)
```

## 前端交互测试

![Pasted image 20231031201713](https://github.com/SuliemNn/S-AES/assets/96652829/67ac821c-71b0-47d3-8d52-76975a053a93)

加密成功！

![Pasted image 20231031201713](https://github.com/SuliemNn/S-AES/assets/96652829/d1d13f66-9f38-4759-b9af-a32b7a40b549)

解密成功！

![Pasted image 20231031201758](https://github.com/SuliemNn/S-AES/assets/96652829/4fb452a3-ea9e-44ca-a804-eb782006c4bf)

暴力破解成功！耗费时间2.19秒

多重加解密


ascii 加解密
![Pasted image 20231031212045](https://github.com/SuliemNn/S-AES/assets/96652829/e7d74513-77a2-44e1-8eb6-2a36d8edf181)

## 交叉测试

跨平台交叉测试：
qt平台结果：
![{RHUXDFY`H%YGMYYH%QN NO](https://github.com/SuliemNn/S-AES/assets/96652829/327cc18e-785a-4556-a22b-c00cf8146792)

己方结果
![G5@HS1Z$ ENNFQZC _}}_Q8](https://github.com/SuliemNn/S-AES/assets/96652829/fafc7323-6b17-4fab-a33e-1360805ab029)
