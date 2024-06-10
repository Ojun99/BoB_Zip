import os 

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Session(app)
db = SQL("sqlite:///bob.db")

@app.route("/")
def index():
    print(session)
    return render_template("main.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        userid = request.form.get("userid")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # 이름, 아이디, 비밀번호, 2차확인이 공백일 경우 return
        if password == None or confirmation == None or username == None or userid == None:
            return render_template("register.html")
        # 비밀번호 1차와 2차가 다르면 return
        if not (password == confirmation):
            return render_template("register.html")
       
        
        # 사용자 이름, 아이디 중복검사
        aaa = db.execute("SELECT * FROM users WHERE userid=?", userid)
        user = db.execute("SELECT * FROM users WHERE username=?", username)
        if len(user) == 1:
            return render_template("register.html")
        elif len(aaa) == 1:
            return render_template("register.html")
        else:
            hashpass = generate_password_hash(password)
            db.execute("INSERT INTO users (username, userid, hash) VALUES(?, ?, ?)", username, userid, hashpass)
            flash("회원가입 되었습니다.")
            return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form.get("userid"):
            return render_template("login.html")
        elif not request.form.get("password"):
            return render_template("login.html")
        
        rows = db.execute("SELECT * FROM users WHERE userid = ?", request.form.get("userid"))
        print(rows)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        if len(session) == 2:
           return redirect("/restaurant")
        return render_template("main.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    flash("로그아웃 되었습니다.")
    # Redirect user to login form
    return redirect("/")



@app.route("/count", methods=["GET", "POST"])
def count():
    r_id = request.form.get("r_id")
    session["r_id"] = r_id
    if request.method == "POST":
        if len(session) == 1:
            flash("로그인이 필요합니다.")
            return render_template("login.html")
        
        menu = db.execute("SELECT * FROM menu WHERE r_id = ?", r_id)
        return render_template("people.html")
        # return render_template("menu.html", menu = menu)
    else:
        return render_template("menu.html")
    
@app.route("/restaurant")
def restaurant():
    rows = db.execute("SELECT * FROM restaurant")
    #r_rows = db.execute("SELECT * FROM menu WHERE r_id = ?", session["r_id"])
    return render_template("test2.html", rows = rows)


@app.route("/restaurant23")
def restaurant23():
    rows2 = db.execute("SELECT * FROM restaurant where id = 2")
    rows3 = db.execute("SELECT * FROM restaurant where id = 3")
    #r_rows = db.execute("SELECT * FROM menu WHERE r_id = ?", session["r_id"])
    return render_template("test23.html", rows2 = rows2, rows3 = rows3)


@app.route("/restaurant45")
def restaurant45():
    rows4 = db.execute("SELECT * FROM restaurant where id = 4")
    rows5 = db.execute("SELECT * FROM restaurant where id = 5")
    #r_rows = db.execute("SELECT * FROM menu WHERE r_id = ?", session["r_id"])
    return render_template("test45.html", rows4 = rows4, rows5 = rows5)

@app.route("/restaurant67")
def restaurant67():
    rows6 = db.execute("SELECT * FROM restaurant where id = 6")
    rows7 = db.execute("SELECT * FROM restaurant where id = 7")
    #r_rows = db.execute("SELECT * FROM menu WHERE r_id = ?", session["r_id"])
    return render_template("test67.html", rows6 = rows6, rows7 = rows7)
    

@app.route("/index1")
def index1():
    return render_template("index.html")

@app.route("/menu", methods=["GET", "POST"])
def menu():
    menu = db.execute("SELECT * FROM menu WHERE r_id = ?", session["r_id"])
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    if request.method == "POST":
        total = request.form.get("total")
        r_menu = request.form.get("menu")
        asdmenu = db.execute("SELECT * FROM menu WHERE  menu = ?", r_menu)
        #print(asdmenu[0]['menu'])
        if r_menu != None:
            db.execute("INSERT INTO u_order (r_id, u_id, o_food, total, team, realtime) values (?,?,?,?,?,?)",session["r_id"], session["user_id"],asdmenu[0]["menu"], int(asdmenu[0]["price"]), int(session["total_people"]), datetime.now())
        if total != None:
            menu_total_price = db.execute("SELECT sum(total) 주문총합 FROM u_order where r_id = ? group by team",session["r_id"])
            menu_total = db.execute("SELECT group_concat(u_order.o_food) from u_order where r_id = ? and u_id = ?",session["r_id"], session["user_id"])
            order_name = db.execute("SELECT username from users WHERE id = ?",session["user_id"])
            order_team = db.execute("SELECT team from u_order where r_id = ? and u_id = ? group by u_id",session["r_id"], session["user_id"])
            flash("예약이 완료되었습니다.")           
            print(order_team)
            return render_template("confirm.html", menu_total_price = menu_total_price, menu_total = menu_total, order_name = order_name, order_team = order_team)
        return render_template("menu.html", menu = menu)
    else:
        return render_template("menu.html", menu = menu)


@app.route("/people", methods=["GET", "POST"])
def people():
    if request.method == "POST":
        people = request.form.get("number")
        session["total_people"] = people
        return redirect("/menu")
    else:
        return render_template("people.html")
    

@app.route("/confirm")
def confirm():
    if len(session) >= 1:
        menu_total_price = db.execute("SELECT sum(total) 주문총합 FROM u_order where u_id = ? group by team",session["user_id"])
        menu_total = db.execute("SELECT group_concat(u_order.o_food) from u_order where u_id = ?", session["user_id"])
        order_name = db.execute("SELECT username from users WHERE id = ?",session["user_id"])
        order_team = db.execute("SELECT team from u_order where u_id = ? group by u_id", session["user_id"])
        return render_template("confirm.html", menu_total_price = menu_total_price, menu_total = menu_total, order_name = order_name, order_team = order_team)
    flash("로그인이 필요한 서비스입니다.") 
    
    return render_template("login.html")