from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()   # 👈 .env read karega

app = Flask(__name__)
app.secret_key = "secret_portfolio_key"

# 🔐 MongoDB URI env se
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['portfolio_db']


@app.route('/')
def index():
    user_data = db.about_me.find_one()

    if not user_data:
        user_data = {
            "name": "Aapka Naam",
            "degree": "B.Tech / Master",
            "experience": "Fresher",
            "email": "example@mail.com",
            "address": "City, India"
        }

    return render_template('index.html', data=user_data)


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    msg_doc = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }

    db.contacts.insert_one(msg_doc)
    flash("Message successfully sent!")
    return redirect('/#contact')


def setup_db():
    if db.about_me.count_documents({}) == 0:
        db.about_me.insert_one({
            "name": "Sneha Gade",
            "degree": "Bachelor In CSE",
            "phone": "8006757633",
            "email": "sgade5591@gmail.com",
            "address": "Bareilly, India",
            "birthday": "4 September 2005"
        })
        print("Initial data inserted!")


if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
