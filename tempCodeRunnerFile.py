from flask import Flask, render_template, request, redirect, url_for, flash
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = "secret123"

DONORS_FILE = "donors.json"

from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Optional email configuration (set these as environment variables in VS Code)
SENDER_EMAIL = os.getenv("SENDER_EMAIL", None)
SENDER_PASS = os.getenv("SENDER_PASS", None)

def send_email(to_email, name, amount, cause):
    """Send a thank-you email if email is configured"""
    if not SENDER_EMAIL or not SENDER_PASS:
        print(f"[INFO] Email not configured. Donation recorded: {name} donated ${amount} for {cause}.")
        return

    try:
        subject = "Thank You for Your Donation!"
        body = f"""
        Dear {name},

        Thank you so much for your generous donation of ${amount} towards {cause}.
        Your support is making a real difference! 🌍💖

        With gratitude,
        Social Good Donations Team
        """

        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.send_message(msg)

        print(f"[SUCCESS] Email sent to {to_email}")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


# Homepage
@app.route("/")
def index():
    return render_template("index.html")


# Donation confirmation
@app.route("/confirm", methods=["POST"])
def confirm():
    name = request.form["name"]
    email = request.form["email"]
    amount = request.form["amount"]
    cause = request.form["cause"]

    # 👇 Call send_email() here
    send_email(email, name, amount, cause)

    return render_template("success.html", name=name, amount=amount, cause=cause)


if __name__ == "__main__":
    app.run(debug=True)

# Load donation history
def load_donors():
    try:
        with open(DONORS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save donation history
def save_donor(donor):
    donors = load_donors()
    donors.append(donor)
    with open(DONORS_FILE, "w") as f:
        json.dump(donors, f, indent=4)

# Send email confirmation
def send_email(to_email, name, amount, cause):
    sender_email = "your_email@gmail.com"
    sender_pass = "your_app_password"  # Use Gmail app password

    subject = "Thank You for Your Donation ❤️"
    body = f"""
    Dear {name},

    Thank you for donating ${amount} towards {cause}.
    Your kindness will make a difference!

    Regards,
    Social Good Donations Team
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email error:", e)


@app.route("/")
def home():
    donors = load_donors()
    return render_template("index.html", donors=donors)


@app.route("/donate", methods=["POST"])
def donate():
    name = request.form["name"]
    email = request.form["email"]
    amount = request.form["amount"]
    cause = request.form["cause"]

    # Redirect to mock payment page
    return render_template("payment.html", name=name, email=email, amount=amount, cause=cause)


@app.route("/confirm", methods=["POST"])
def confirm():
    name = request.form["name"]
    email = request.form["email"]
    amount = request.form["amount"]
    cause = request.form["cause"]

    # Save donor details
    donor = {"name": name, "email": email, "amount": amount, "cause": cause}
    save_donor(donor)

    # Send confirmation email
    send_email(email, name, amount, cause)

    return render_template("success.html", donor=donor, donors=load_donors())


if __name__ == "__main__":
    app.run(debug=True)