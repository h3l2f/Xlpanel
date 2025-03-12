# type: ignore
from __main__ import *
import time
import ende
import db
import random

_chr = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"

@app.route("/forgot/", methods=["GET", "POST"])
def fg():
    if request.method == "GET":
        return render_template(
            "forgot.html",
            name=name,
        )
    elif request.method == "POST":
        email = request.form.get("email","")
        conn = db.connect()
        cursor = conn.cursor()
        
        cursor.execute("select lastSend from user where email=?", (email,))
        e = cursor.fetchall()
        if len(e)==0:
            return jsonify({"status":"error", "message": "Email not found."})
        ls = e[0][0]
        if (ls > time.time()-3600):
            return jsonify({"status":"error", "message": f"Please wait {-int(time.time())+3600+ls}s!"})
        nw = "".join(random.choice(_chr) for i in range(random.randint(10, 15)))
        e = sendmail.sendrspwd(email, nw)
        if (e[0]):
            cursor.execute("update user set password=?, lastSend=? where email=?", (ende.encode(nw), int(time.time()),email))
            conn.commit()
            conn.close()
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status":"error", "message": f"Something went wrong!"})