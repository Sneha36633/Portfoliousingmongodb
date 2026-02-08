from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 🔐 Load .env (Sirf local development ke liye)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# 🔐 MongoDB URI: Pehle system environment check karega (Render), phir .env
mongo_uri = os.environ.get("MONGO_URI")

# Agar dono jagah nahi mila, tab error dikhayein bina crash kiye
if not mongo_uri:
    print("⚠️ WARNING: MONGO_URI not found in environment variables!")

# 🔗 MongoDB Connection
try:
    # TLS/SSL errors se bachne ke liye srv support zaroori hai
    client = MongoClient(mongo_uri)
    client.admin.command('ping')
    print("✅ MongoDB connected successfully")
    db = client["portfolio_db"]
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    db = None # App crash nahi hogi, handle karega

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    user_data = None
    if db is not None:
        user_data = db.about_me.find_one()

    if not user_data:
        user_data = {
            "name": "Sneha Gade",
            "degree": "Bachelor in CSE",
            "experience": "Fresher",
            "email": "sgade5591@gmail.com",
            "address": "Bareilly, India"
        }

    return render_template('index.html', data=user_data)


@app.route('/contact', methods=['POST'])
def contact():
    if db is None:
        flash("❌ Database not connected!")
        return redirect('/#contact')

    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

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
    if db is not None and db.about_me.count_documents({}) == 0:
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
    # Render ke liye dynamic port zaroori hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)