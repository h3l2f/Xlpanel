# type: ignore
from __main__ import *
import time
import random

welSen = [
    "Welcome to your Dashboard, {user}!",
    "Dashboard loaded, {user}! Explore your overview.",
    "Welcome back to your Dashboard page, {user}.",
    "Your Dashboard is ready, {user}. See your key stats.",
    "Greetings, {user}! Your Dashboard awaits your review.",
    "Welcome, {user}! Dive into your Dashboard's summary.",
    "Dashboard access granted, {user}! Welcome.",
    "Welcome to the central overview of your Dashboard, {user}.",
    "Your Dashboard is now active, {user}.",
    "Welcome, {user}! See your most important metrics at a glance on your Dashboard.",
    "Dashboard initialized, {user}. Welcome!",
    "Welcome to your personalized Dashboard, {user}.",
    "Your Dashboard is here, {user}. What do you want to see first?",
    "Dashboard loaded successfully, {user}. Welcome!",
    "Welcome to the front page of your Dashboard, {user}.",
    "Your Dashboard is online, {user}. Welcome!",
    "Welcome, {user}! Let's review your overall progress on your Dashboard.",
    "Dashboard view activated, {user}. Welcome!",
    "Welcome to your streamlined Dashboard experience, {user}.",
    "Your Dashboard has been updated, {user}. Welcome!",
    "Welcome, {user}! Your Dashboard is your starting point.",
    "Dashboard access confirmed, {user}. Welcome!",
    "Welcome to your overview Dashboard, {user}.",
    "Your Dashboard is now live, {user}. Welcome!",
    "Welcome, {user}! Get a quick overview from your Dashboard.",
    "Dashboard entry confirmed, {user}. Welcome!",
    "Welcome to your summary Dashboard, {user}.",
    "Your Dashboard is ready for your quick analysis, {user}. Welcome!",
    "Welcome, {user}! Your Dashboard gives you a bird's-eye view.",
    "Dashboard loaded, {user}. Welcome to your main view.",
    "Welcome, {user}! Your Dashboard is designed for quick insights.",
    "Your Dashboard is now accessible, {user}. Welcome!",
    "Welcome to your informative Dashboard, {user}.",
    "Dashboard access successful, {user}. Welcome!",
    "Welcome, {user}! Your Dashboard is your initial briefing.",
    "Your Dashboard is primed and ready, {user}. Welcome!",
    "Welcome to your powerful Dashboard overview, {user}.",
    "Dashboard connection established, {user}. Welcome!",
    "Welcome, {user}! Your Dashboard sets the stage for your work.",
    "Your Dashboard is now in focus, {user}. Welcome!",
    "Welcome to your comprehensive Dashboard summary, {user}.",
    "Your Dashboard is ready for your quick start, {user}. Welcome!",
    "Welcome to your user-friendly Dashboard, {user}.",
    "Dashboard interface loaded, {user}. Welcome!",
    "Welcome, {user}! Your Dashboard gives you a quick snapshot.",
    "Your Dashboard is now available, {user}. Welcome!",
    "Welcome to your dynamic Dashboard page, {user}."
]

@app.route("/dashboard/", methods=["GET"])
def dashboard():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")

        hour = int(datetime.datetime.now().strftime("%H"))
        bigWel = f"""Good {"midnight" if 0<=hour<5 else "morning" if 5<=hour<=12 else "afternoon" if 13<=hour<=17 else "evening"}!"""
        smallWel = random.choice(welSen).format(user=check[1]["user"])
        uSv = helper.listPteroServer(check[1]["user"])
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uSv[0] == False) or (uDt[0] == False):
            return f"""Something went wrong!\n\nuSv response:\n{uSv}\n\nuDt response:\n{uDt}"""

        return render_template(
            "dash.html",
            name=name,
            bigWel=bigWel,
            smallWel=smallWel,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            cpu=check[1]["cpu"]-uSv[2],
            ram=check[1]["ram"]-uSv[4],
            disk=check[1]["disk"]-uSv[3],
            slot=check[1]["slot"]-len(uSv[1]),
            coin=check[1]["coin"],
            dcpu=check[1]["cpu"],
            dram=check[1]["ram"],
            ddisk=check[1]["disk"],
            dslot=check[1]["slot"],
            mIt=menuItems,
            loadTime=int((time.time()-beginT)*100000)/100000
        )