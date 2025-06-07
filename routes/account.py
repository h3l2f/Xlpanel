# type: ignore
from __main__ import *
import time
import ende
import db

@app.route("/account/", methods=["GET"])
def yacc():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""

        return render_template(
            "account.html",
            name=name,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            coin=check[1]["coin"],
            error = request.args.get("err", None),
            mIt=menuItems,
            loadTime=int((time.time()-beginT)*100000)/100000
        )

@app.route("/account/ptero/", methods=["GET"])
def pteroPwd():
    if request.method == "GET":
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        e = helper.checkPteroUser(check[1]["user"])
        e = helper.getPteroPasswd(e)
        if e[0]:
            return jsonify({"status":"ok", "passwd": e[1]})
        else:
            return jsonify({"status":"error", "message": e[1]})

@app.route("/account/change/", methods=["POST"])
def accChange():
    if request.method == "POST":
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        
        crpwd = request.form.get("crpasswd","")
        nwpwd = request.form.get("nwpasswd","")
        cnwpwd = request.form.get("cnwpasswd","")
        if (
            (not crpwd)
            or
            (not nwpwd)
            or
            (not cnwpwd)
        ):
            return redirect(f"/account?err=Missing data.")
        elif (nwpwd != cnwpwd):
            return redirect(f"/account?err=Please confirm your new password.")
        
        l = ende.checkpw(check[1]["pwd"], crpwd)
        if (not l):
            return redirect(f"/account?err=Invalid current password.")
        elif (crpwd == nwpwd):
            return redirect(f"/account?err=changed")
        else:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("update user set password=? where user=?", (ende.encode(nwpwd),check[1]["user"]))
            conn.commit()
            conn.close()
            return redirect(f"/account?err=changed")