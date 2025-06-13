# type: ignore
from __main__ import *
import time
import db

from flask import redirect, render_template

@app.route("/admin/", methods=["GET"])
def ad():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""

        if (uDt[1].get("root_admin",False)):
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("select user, coin, cpu, disk, ram, banned from user")
            e = cursor.fetchall()
            conn.close()
            return render_template(
                "admin.html",
                name=name,
                isAdmin=uDt[1].get("root_admin",False),
                user=check[1]["user"],
                coin=check[1]["coin"],
                mIt=menuItems,
                ul=e,
                error=request.args.get("err"),
                version=ver,
                codename=codename,
                loadTime=int((time.time()-beginT)*100000)/100000
            )
        else:
            abort(403)

@app.route("/admin/add/", methods=["GET"])
def adr():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""

        if (uDt[1].get("root_admin",False)):
            user = request.args.get("user", "")
            cpu = request.args.get("cpu", "0")
            ram = request.args.get("ram", "0")
            disk = request.args.get("disk", "0")
            slot = request.args.get("slot", '0')
            coin = request.args.get("coin", "0")

            if (not cpu): cpu = "0"
            if (not ram): ram = "0"
            if (not disk): disk = "0"
            if (not slot): slot = "0"
            if (not coin): coin = "0"
            try:
                cpu = int(cpu)
            except Exception: cpu = 0
            try:
                ram = int(ram)
            except Exception: ram = 0
            try:
                disk = int(disk)
            except Exception: disk = 0
            try:
                slot = int(slot)
            except Exception: slot = 0
            try:
                coin = int(coin)
            except Exception: coin = 0

            u = helper.getUser(user)
            if not u[0]:
                return redirect("/admin?err=User not found.")
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("update user set cpu=cpu+?, ram=ram+?, disk=disk+?, slot=slot+?, coin=coin+? where user=?",(cpu, ram, disk, slot, coin, user))
            conn.commit()
            conn.close()
            return redirect("/admin?err=none")
        else:
            abort(403)

@app.route("/admin/ban/<user>/", methods=["GET"])
def _adb(user):
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""

        if (uDt[1].get("root_admin",False)):
            if check[1]["user"] == user:
                return redirect("/admin?err=You can't ban yourself.")
            u = helper.getUser(user)
            if not u[0]:
                return redirect("/admin?err=User not found.")
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("update user set banned = ? where user=?",(int(not u[1]["banned"]), user))
            conn.commit()
            conn.close()
            return redirect("/admin?err=none")
        else: abort(403)