#type: ignore
from __main__ import *

@app.errorhandler(HTTPException)
def HTTPError(e):
    if ("application/json" in request.headers.get("accept","").split(",")):
        return jsonify({"status": "error", "message": f"{str(e.code)} - {e.name}", "description": e.description}), int(e.code)
    return render_template("HTTPerror.html",    errorCode=str(e.code), errorName=e.name, errorDes = e.description), int(e.code)