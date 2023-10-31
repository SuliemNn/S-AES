import S_AES
from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#普通加密
@app.route('/enCrypt',methods=['POST'])
def webEnCrypt():
    data=eval(request.get_data().decode("utf-8"))
    print(data)
    return S_AES.enCrypt(data["plainText"],data["key"])

#普通解密
@app.route('/deCrypt',methods=['POST'])
def webDeCrypt():
    data = eval(request.get_data().decode("utf-8"))
    print(data)
    return S_AES.deCrypt(data["cyberText"],data["key"])


#多重加密
@app.route('/multiplyEnCrypt', methods=['POST'])
def webmultiplyEeCrypt():
    data = eval(request.get_data().decode("utf-8"))
    print(data)
    return S_AES.multiplyEnCrypt(data["plainText"], data["key"])

#多重解密
@app.route('/multiplyDeCrypt', methods=['POST'])
def webmultiplyDeCrypt():
    data = eval(request.get_data().decode("utf-8"))
    print(data)
    return S_AES.multiplyDeCrypt(data["cyberText"], data["key"])


#暴力破解的ajax请求
@app.route('/breakOut', methods=['POST'])
def webBreakOut():
    data = eval(request.get_data().decode("utf-8"))
    print(data)
    result=S_AES.breakOut(data["plainText"],data["cyberText"])
    print(result)
    return  jsonify({"result":result[0],"time":result[1]})

#ascii加密的ajax请求
@app.route('/asciiEnCrypt',methods=['POST'])
def webAsciiEnCrypt():
    data = eval(request.get_data().decode("utf-8"))
    print(data)
    result=S_AES.asciiEnCrypt(data["plainText"],data["key"])
    return jsonify({"result":result})

#ascii解密的ajax请求
@app.route('/asciiDeCrypt',methods=['POST'])
def webAsciiDeCrypt():
    data = eval(request.get_data().decode("utf-8"))
    print(data)
    result=S_AES.asciiDeCrypt(data["cyberLst"],data["key"])
    return result


# @app.route('/getCity', methods=['POST'])
# def submit():
#     cursor = db.cursor()
#     data = request.get_data()
#
#     # 将二进制数据解码为字符串
#     decoded_data = data.decode('utf-8')
#     decoded_data = eval(decoded_data)["tempdata"]
#
#     cursor.execute("select cityname from provinfo where provname = %s",(decoded_data,))
#     result=cursor.fetchall()
#     print(result)
#
#
#     db.commit()
#     cursor.close()
#
#     return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
