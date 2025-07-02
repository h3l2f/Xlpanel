# type: ignore
from __main__ import *
import time

from flask import jsonify
import ende
import db
import io
import random
import string
from captcha.image import ImageCaptcha
import base64

captLen = config["captcha"]["captchaLength"]
if type(captLen) != int: captLen=6
captRec = config["captcha"]["coinPerSolve"]
if type(captRec) != int: captRec=1
captRL = config["captcha"]["limitPerMinute"]
if type(captRL) != int: captRL=6

@app.route("/captcha/", methods=["GET"])
def capt4coin():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""
        return render_template(
            "captcha.html",
            name=name,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            coin=check[1]["coin"],
            captRec=captRec,
            captLen=captLen,
            mIt=menuItems,
            loadTime=int((time.time()-beginT)*100000)/100000
        )

sovTk = {}

@app.route("/captGen/", methods=["GET"])
@limiter.limit(
    f"{captRL} per minute",
    key_func=lambda: request.cookies.get("sid", "nokey"),
    error_message=f"Reached the limit of requests per minute. ({captRL}/min)"
    )
def _captgen():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
    
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=captLen))
    realToken = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=20))
    fakeToken = ''.join(random.choices(string.ascii_uppercase + string.ascii_uppercase + string.digits, k=34))
    image_generator = ImageCaptcha(
        width=280,
        height=90,
        font_sizes=[30, 35, 40], #pyright: ignore
        fonts=["assets/font/jetbrains-mono.ttf"]
        )

    image_data_file = image_generator.generate(captcha_text)

    img_io = io.BytesIO(image_data_file.read())
    img_io.seek(0)

    image_bytes = img_io.getvalue()

    base64_encoded_bytes = base64.b64encode(image_bytes)
    base64_string = base64_encoded_bytes.decode('utf-8')

    resp = jsonify({"status":"ok","image": base64_string, "token": fakeToken})
    resp.headers["CF-CONNECT-TOKEN"] = realToken
    sovTk[realToken] = {
        "user": check[1]["user"],
        "capt": captcha_text
    }
    return resp

@app.route("/captSol/", methods=["GET"])
@limiter.limit(
    f"{captRL} per minute",
    key_func=lambda: request.cookies.get("sid", "nokey"),
    error_message=f"Reached the limit of requests per minute. ({captRL}/min)"
    )
def captsol():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        def decode(s:str):
            ech = {
                "000000": "A", 
                "000001": "B", 
                "000010": "C",
                "000011": "D",
                "000100": "E", 
                "000101": "F", 
                "000110": "G",
                "000111": "H",
                "001000": "I",
                "001001": "J",
                "001010": "K", 
                "001011": "L", 
                "001100": "M",
                "001101": "N",
                "001110": "O",
                "001111": "P",
                "010000": "Q",
                "010001": "R",
                "010010": "S",
                "010011": "T",
                "010100": "U",
                "010101": "V",
                "010110": "W",
                "010111": "X",
                "011000": "Y",
                "011001": "Z",
                "011010": "a",
                "011011": "b",
                "011100": "c",
                "011101": "d",
                "011110": "e",
                "011111": "f",
                "100000": "g",
                "100001": "h",
                "100010": "i",
                "100011": "j",
                "100100": "k",
                "100101": "l",
                "100110": "m",
                "100111": "n",
                "101000": "o",
                "101001": "p",
                "101010": "q",
                "101011": "r",
                "101100": "s",
                "101101": "t",
                "101110": "u",
                "101111": "v",
                "110000": "w",
                "110001": "x",
                "110010": "y",
                "110011": "z",
                "110100": "0",
                "110101": "1",
                "110110": "2",
                "110111": "3",
                "111000": "4",
                "111001": "5",
                "111010": "6",
                "111011": "7",
                "111100": "8",
                "111101": "9",
                "111110": "+",
                "111111": "/"
            }
            bn = list(ech.keys())
            vl = list(ech.values())

            ls = []
            en = list(s)
            for i in range((len(en)//2)*2):
                if i%2!=0: continue
                en[i], en[i+1] = en[i+1], en[i]
            s = "".join(en)
            b = list("".join(bn[vl.index(i)] for i in s))
            while (len(b)%8!=0): del b[len(b)-1]
            b = "".join(b)
            for i in range(1,len(b)//8+1):
                ls.append(b[(i*8)-8: i*8])
            return "".join([chr(int(i, 2)) for i in ls])
        try:
            e = decode(request.args.get("val").replace("\\",""))
        except Exception:
            return jsonify({"status": "error", "message": "Internal server error."})

        e = e.split(" ")
        if len(e)!=2: 
            return jsonify({"status": "error", "message": "Invalid token."})
        token =e[1]
        capt = e[0]

        if token not in list(sovTk.keys()):
            return jsonify({"status": "error", "message": "Invalid token."})
        elif sovTk[token]["capt"] != capt:
            sovTk.pop(token)
            return jsonify({"status": "error", "message": "Wrong answer."})
        else:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("update user set coin=coin+? where user=?", (captRec, sovTk[token]["user"]))
            conn.commit()
            conn.close()
            sovTk.pop(token)
            return jsonify({"status": "ok", "rcv": captRec})
