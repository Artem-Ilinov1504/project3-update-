from flask import (Flask, render_template,
                   request, redirect, url_for, make_response)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Ordinary_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(200), nullable=False)

class Favorites_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(200), nullable=False)

class Secret_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(200), nullable=False)

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["hashedPassword"]
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', username)
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ordinary")
def ordinary():
    ordinary_records = Ordinary_record.query.all()
    return render_template("ordinary.html", ordinary_records=ordinary_records)

@app.route("/favorites")
def favorites():
    favorites_records = Favorites_record.query.all()
    return render_template("favorites.html", favorites_records=favorites_records)

@app.route("/secret")
def secret():
    return render_template("secret.html")

@app.route("/ordinary", methods=["POST"])
def add_ordinary_record():
    if request.method == "POST":
        name = request.form["ordinary_name"]
        text = request.form["ordinary_text"]
        new_ordinary_record = Ordinary_record(name=name, text=text)
        db.session.add(new_ordinary_record)
        db.session.commit()
        response = make_response(redirect(url_for('ordinary')))
        return response

@app.route("/delete_ordinary", methods=["POST"])
def delete_ordinary_record():
    if request.method == "POST":
        id = request.form["id"]
        Ordinary_record.query.filter_by(id=id).delete()
        db.session.commit()
        response = make_response(redirect(url_for('ordinary')))
        return response

@app.route("/favorites", methods=["POST"])
def add_favorites_record():
    if request.method == "POST":
        name = request.form["favorites_name"]
        text = request.form["favorites_text"]
        new_favorites_record = Favorites_record(name=name, text=text)
        db.session.add(new_favorites_record)
        db.session.commit()
        response = make_response(redirect(url_for('favorites')))
        return response

@app.route("/delete_favorites", methods=["POST"])
def delete_favorites_record():
    if request.method == "POST":
        id = request.form["id"]
        Favorites_record.query.filter_by(id=id).delete()
        db.session.commit()
        response = make_response(redirect(url_for('favorites')))
        return response

@app.route("/secret", methods=["POST"])
def add_secret_record():
    if request.method == "POST":
        name = request.form["secret_name"]
        text = request.form["secret_text"]
        new_secret_record = Secret_record(name=name, text=text)
        db.session.add(new_secret_record)
        db.session.commit()
        response = make_response(redirect(url_for('secret')))
        return response

@app.route("/delete_secret", methods=["POST"])
def delete_secret_record():
    if request.method == "POST":
        id = request.form["id"]
        Secret_record.query.filter_by(id=id).delete()
        db.session.commit()
        response = make_response(redirect(url_for('secret')))
        return response


@app.route("/autorization")
def autorization():
    return render_template("autorization.html")



@app.route("/autorizate", methods=["POST"])
def autorizate():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['hashedPassword']
            names = User.query.all()
            print(names)
            if username in names and names[username].password == password:
                response = make_response(redirect(url_for('secret')))
                response.set_cookie('username', username)
                return response
            else:
                return render_template('index.html')
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)