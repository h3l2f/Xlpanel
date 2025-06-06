# type: ignore
from __main__ import *
import time
import db

@app.route("/store/", methods=["GET"])
def _store():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""

        return render_template(
            "store.html",
            name=name,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            mIt=menuItems,
            coin=check[1]["coin"],
            store=store,
            
            
            
            error=request.args.get("err"),
            loadTime=int((time.time()-beginT)*100000)/100000
        )

@app.route("/store/buy/", methods=["GET"])
def _buy():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        item = request.args.get("item")
        print(item)
        amount = request.args.get("amount")
        if item not in ["cpu", "ram", "disk", "slot"]:
            return redirect("/store?err=Invalid item.")
        elif not amount.isdigit():
            return redirect("/store?err=Invalid data type.")
        if (store[item][0]*int(amount)) > check[1]["coin"]:
            return redirect("/store?err=Not enough coins.")
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(f"update user set {item}={item}+? where user=?",(store[item][1]*int(amount), check[1]["user"]))
        cursor.execute(f"update user set coin=coin-? where user=?",(store[item][0]*int(amount), check[1]["user"]))
        conn.commit()
        conn.close()
        return redirect("/store?err=none")