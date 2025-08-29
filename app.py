from flask import Flask, render_template, request, redirect, url_for
import json
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv   # ✅ add this

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Load donors from JSON file
def load_donors():
    try:
        with open("donors.json", "r") as f:
            return json.load(f)
    except:
        return []

# Save donors to JSON file
def save_donor(donor):
    donors = load_donors()
    donors.insert(0, donor)
    with open("donors.json", "w") as f:
        json.dump(donors, f, indent=4)

# Optional: Send confirmation email
def send_email(to_email, subject, message):
    try:
        sender_email = os.getenv("MAIL_USERNAME")    # ✅ now from .env
        sender_password = os.getenv("MAIL_PASSWORD") # ✅ now from .env

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Email sending failed:", e)

# Homepage → Donation form + donor list
@app.route("/")
def home():
    donors = load_donors()
    return render_template("index.html", donors=donors)

# Donation form submit → go to fake payment page
@app.route("/pay", methods=["POST"])
def pay():
    donor = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "amount": request.form.get("amount"),
        "cause": request.form.get("cause")
    }
    return render_template("payment.html", donor=donor)

# Fake payment → Success page
@app.route("/success", methods=["POST"])
def success():
    donor = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "amount": request.form.get("amount"),
        "cause": request.form.get("cause")
    }

    # Save donor info
    save_donor(donor)

    # Send email if provided
    if donor["email"]:
        message = f"Dear {donor['name']},\n\nWe extend our heartfelt gratitude for your generous donation of ${donor['amount']} towards {donor['cause']}.\nYour support plays a crucial role in advancing our mission and creating a positive impact.\n\nEvery contribution, no matter the size, brings us closer to achieving our goals. Thanks to compassionate individuals like you, we can continue to make a difference in the lives of many.\n\nAs a token of our appreciation, we would like to keep you updated on the progress of our initiatives and the impact your donation is making. You can stay connected with us through our website and social media channels.\n\nThank you once again for your kindness and generosity. Together, we can build a better future.\n\nWith sincere appreciation,\nThe Unity Hands Team ❤️"
        send_email(donor["email"], "Thank You for Your Donationt", message)

    return render_template("success.html", donor=donor)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
