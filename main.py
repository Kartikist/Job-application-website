from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "neti.kartik@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")
db = SQLAlchemy(app)
mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        email = request.form["email"]
        occupation = request.form["occupation"]
        form = Form(first_name = first_name, last_name = last_name, date= date_obj  , email = email, occupation = occupation)
        db.session.add(form)
        db.session.commit()
        body_message = f"Thank you {first_name} for your submission"
        print(email)
        message = Message(subject="New form entry", sender=app.config["MAIL_USERNAME"], recipients=[email], body = body_message )
        mail.send_message(message)
        flash("FORM SUCCESS", "success")
      
            
    return render_template("index.html")



if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)