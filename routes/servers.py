# type: ignore
from __main__ import *
import time

@app.route("/servers/", methods=["GET"])
def servers():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        uSv = helper.listPteroServer(check[1]["user"])
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uSv[0] == False) or (uDt[0] == False):
            return f"""Something went wrong!\n\nuSv response:\n{uSv}\n\nuDt response:\n{uDt}"""

        return render_template(
            "server.html",
            name=name,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            sv = uSv[1],
            error = request.args.get("err", None),
            eggs=eggsList,
            nodes=nodeList,
            mIt=menuItems,
            
            
            
            coin=check[1]["coin"],
            loadTime=int((time.time()-beginT)*100000)/100000
        )

@app.route("/server/<identity>/", methods=["GET", "DELETE"])
def _sv(identity: str):
    beginT = time.time()
    check = helper.chSID(request.cookies.get("sid"))
    if (not check[0]):
        return redirect("/login")
    uSv = helper.listPteroServer(check[1]["user"])
    uDt = helper.checkPteroUser(check[1]["user"])
    if request.method == "GET":
        if (uSv[0] == False) or (uDt[0] == False):
            return f"""Something went wrong!\n\nuSv response:\n{uSv}\n\nuDt response:\n{uDt}"""
        for i in uSv[1]:
            if i["identifier"] == identity:
                return render_template(
                    "iserver.html",
                    name=name,
                    isAdmin=uDt[1].get("root_admin",False),
                    user=check[1]["user"],
                    i=i,
                    
                    
                    
                    mIt=menuItems,
                    coin=check[1]["coin"],
                    loadTime=int((time.time()-beginT)*100000)/100000
                )
        return render_template(
            "iserver.html",
            name=name,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            error=1,
            
            
            
            mIt=menuItems,
            coin=check[1]["coin"],
            loadTime=int((time.time()-beginT)*100000)/100000
        )
    elif request.method == "DELETE":
        for i in uSv[1]:
            if i["identifier"] == identity:
                if i["status"] == "suspended":
                    return jsonify({"status": "error", "message": "This server has been suspended."})
                e = helper.delPteroServer(i["id"])
                if (e[0]):
                    return jsonify({"status": "ok"})
                else:
                    return jsonify({"status": "error", "message": str(e[1])})
        return jsonify({"status": "error", "message": "You don't have permission to modify this server."})
