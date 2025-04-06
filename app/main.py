from flask import Flask, request, render_template, url_for, redirect, session, make_response

from config import SECRET_KEY, DATABASE
from database import Database

app = Flask(__name__)
app.secret_key = SECRET_KEY

db = Database(DATABASE)

db.init_database()
try:
    db.insert_user("pikvic@list.ru")
except:
    pass

@app.get("/")
def index():
    email = session.get('email')
    if not email:
        return render_template('index.html')
    else:
        return redirect(url_for("me"))

@app.get("/me")
def me():
    email = session.get("email")
    print("me email", email)
    if not email:
        redirect(url_for('index'))
    number = db.get_number(email)
    return render_template('number.html', number=number)

@app.get("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.post("/")
def index_post():
    print(request.form)
    if request.form:
        email = request.form.get("email", None)
        if not email:
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