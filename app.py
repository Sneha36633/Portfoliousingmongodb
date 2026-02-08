from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 🔐 Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_portfolio_key"

# 🔐 MongoDB URI
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise Exception("❌ MONGO_URI not found in .env file")

print("✅ MONGO_URI loaded")

# 🔗 MongoDB Connection
try:
    client = MongoClient(mongo_uri)
    client.admin.command('ping')
    print("✅ MongoDB connected successfully")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise e

db = client["portfolio_db"]

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    user_data = db.about_me.find_one()

    if not user_data:
        user_data = {
            "name": "Your Name",
            "degree": "Your Degree",
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

    # ❗ validation
    if not name or not email or not message:
        flash("Please fill all required fields!")
        return redirect('/#contact')

    msg_doc = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }

    db.contacts.insert_one(msg_doc)
    flash("✅ Message successfully sent!")
    return redirect('/#contact')


# ---------------- INITIAL DATA ---------------- #

def setup_db():
    if db.about_me.count_documents({}) == 0:
        db.about_me.insert_one({
            "name": "Sneha Gade",
            "degree": "Bachelor in CSE",
            "phone": "8006757633",
            "email": "sgade5591@gmail.com",
            "address": "Bareilly, India",
            "birthday": "4 September 2005"
        })
        print("✅ Initial about_me data inserted")


# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
