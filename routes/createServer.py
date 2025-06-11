# type: ignore
from __main__ import *
import time
import random

@app.route("/servers/create/", methods=["GET"])
def crsv():
    if request.method == "GET":
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        name = request.args.get("name")
        cpu = request.args.get("cpu")
        ram = request.args.get("ram")
        disk = request.args.get("disk")
        node = request.args.get("node")
        egg = request.args.get("egg")

        if (
            (not cpu.isdigit())
            or
            (not ram.isdigit())
            or
            (not disk.isdigit())
        ): return redirect(f"/servers?err=invalid data type.")
        elif (
            (int(cpu) == 0)
            or
            (int(ram) == 0)
            or
            (int(disk) == 0)
        ): return redirect(f"/servers?err=Hi lil exploiter.")

        r = helper.createPteroServer(name, check[1]["user"], node, egg, int(cpu), float(ram), float(disk))
        if not r[0]: return redirect(f"/servers?err={r[1]}")
        else: return redirect(f"/servers?err=none")