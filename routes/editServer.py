# type: ignore
from __main__ import *
import time
import random

@app.route("/server/<_id>/edit/", methods=["GET"])
def editSv(_id):
    if request.method == "GET":
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        cpu = request.args.get("cpu","")
        ram = request.args.get("ram","")
        disk = request.args.get("disk","")

        if (
            (not cpu.isdigit())
            or
            (not ram.isdigit())
            or
            (not disk.isdigit())
        ): return redirect(f"/server/{_id}?err=invalid data type.")
        elif (
            (int(cpu) == 0)
            or
            (int(ram) == 0)
            or
            (int(disk) == 0)
        ): return redirect(f"/server/{_id}?err=Hi lil exploiter.")

        r = helper.editPteroServer(check[1]["user"], _id, int(cpu), int(ram), int(disk))
        if not r[0]: return redirect(f"/server/{_id}?err={r[1]}")
        else: return redirect(f"/server/{_id}?err=none")
