from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 🔐 Environment Variables load karein (Local ke liye .env, Render ke liye Dashboard)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secret_portfolio_key")

# 🔐 MongoDB URI: Dono jagah (Local/Render) CAPS mein hona zaroori hai
mongo_uri = os.environ.get("MONGO_URI")

# Debugging lines (Terminal mein check karne ke liye)
if not mongo_uri:
    print("⚠️ WARNING: MONGO_URI not found in environment variables!")
else:
    print(f"✅ MONGO_URI detected: {mongo_uri[:15]}...")

# 🔗 MongoDB Connection Logic
db = None
if mongo_uri:
    try:
        # 'serverSelectionTimeoutMS' timeout set karta hai taaki app hang na ho
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB connected successfully")
        db = client["portfolio_db"]
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    user_data = None
    if db is not None:
        try:
            user_data = db.about_me.find_one()
        except Exception:
            user_data = None

    # Fallback data agar DB se nahi milta
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

    try:
        msg_doc = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message
        }
        db.contacts.insert_one(msg_doc)
        flash("✅ Message successfully sent!")
    except Exception as e:
        flash(f"❌ Error saving message: {e}")

    return redirect('/#contact')


# ---------------- INITIAL DATA SETUP ---------------- #

def setup_db():
    if db is not None:
        try:
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
        except Exception as e:
            print(f"⚠️ Could not setup initial data: {e}")


# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    setup_db()
    # 🚀 Render ke liye Host aur Port binding mandatory hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)