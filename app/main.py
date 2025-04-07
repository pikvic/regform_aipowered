from flask import Flask, request, render_template, url_for, redirect, session, make_response, send_file, Response

from config import SECRET_KEY, DATABASE, SUPERADMIN
from database import Database
import csv

from email.utils import parseaddr

app = Flask(__name__)
app.secret_key = SECRET_KEY

db = Database(DATABASE)

db.init_database()

def is_valid_email(email):
    mail = parseaddr(email)[-1]
    if not mail:
        return False
    if not "@dvfu.ru" in mail:
        return False
    return True

def parse_csv():
    with open('data.csv', encoding="utf-8") as csvfile:
        #fieldnames = ['first_name', 'last_name']
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = list(row.values())[5]
            if is_valid_email(email):
                db.insert_user(email)
   
@app.get("/")
def index():
    email = session.get('email')
    if not email:
        return render_template('index.html', message=None)
    else:
        return redirect(url_for("me"))

@app.get("/me")
def me():
    email = session.get("email")
    if not email:
        return redirect(url_for('index'))
    number = db.get_number(email)
    return render_template('number.html', number=number)

@app.get("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.post("/")
def index_post():
    if request.form:
        email = request.form.get("email", None)
        
        if not email or not is_valid_email(email):
            # show index with error message
            return redirect(url_for('index'))
        user_id = db.get_user_id(email)
        print("user_id", user_id)
        if not user_id:
            # show index with error message
            return redirect(url_for('index'))
        session["email"] = email
        number = db.get_number(email)
        print("number", number)
        if not number:
            db.insert_number(user_id)
            number = db.get_number(email)
            # set cookie, show number
            return redirect(url_for('me'))
        
        #show number
        return redirect(url_for('me'))
    return redirect(url_for('index'))

@app.post("/admin/login")
def admin_login():
    secret = request.form.get("secret")
    if secret == SUPERADMIN:
        session["secret"] = "true"
    return redirect(url_for('admin'))

@app.get("/admin/logout")
def admin_logout():
    session.pop('secret', None)
    return redirect(url_for('admin'))

@app.get("/admin")
def admin():
    secret = session.get("secret")
    logged = False
    if not secret or secret != "true":
        return render_template('admin.html', logged=logged)
    logged = True
    users = db.get_users_numbers()
    return render_template('admin.html', users=users, logged=logged)

@app.post("/admin/upload")
def upload_post():
    secret = session.get("secret")
    if not secret or secret != "true":
        return redirect(url_for('admin'))
    f = request.files['file']
    f.save('data.csv')
    parse_csv()
    return redirect(url_for('admin', secret=secret))

@app.get("/admin/download")
def download():
    secret = session.get("secret")
    if not secret or secret != "true":
        return redirect(url_for('index'))
    users = db.get_users_numbers()
    path = "download.csv"
    with open(path, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "email", "number"])
        for user in users:
            writer.writerow([user["id"], user["email"], user["number"]])
        
    return send_file(path, as_attachment=True)

@app.post("/admin/insert")
def admin_insert():
    referrer = request.headers.get("referrer")
    email = request.get_data().decode("utf-8")
    email = parseaddr(email)[-1]
    if not email or referrer != "yandex":
        return "Not inserted", 200
    if is_valid_email(email):
        db.insert_user(email)
    return "Inserted", 200