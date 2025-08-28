🌍 W9 Donation Website

A simple donation platform built with Flask (Python) that allows people to donate towards different causes like Clean Water, Food Support, Education, and Healthcare.

It includes:

🎨 A modern, responsive frontend.

💳 A fake payment gateway for testing donations.

📧 Automatic email receipts (via Gmail SMTP).

📜 Donor list display on the homepage.



---

✨ Features

Homepage with banner & inspirational quotes 🌟

Select causes (Clean Water, Food Support, Education, Healthcare)

Donation form with preset & custom amounts

Fake payment gateway simulation (no real money)

Auto-email receipt (if email is configured)

List of recent donors shown on homepage



---

📂 Project Structure

W9-Donation/
│
├── app.py               # Flask backend
├── templates/
│   └── index.html       # Homepage template
└── static/
    └── style.css        # Styling


---

🚀 Setup Instructions

1. Clone the Repository

git clone https://github.com/your-username/W9-Donation.git
cd W9-Donation

2. Install Dependencies

pip install flask flask-mail

3. Configure Email (Optional for Receipts)

If you want auto-email to work:

1. Enable 2-Step Verification in your Gmail.


2. Go to Google Account → Security → App Passwords.


3. Generate an app password and use it in app.py:



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

4. Run the Server

python app.py

Then open:
👉 http://127.0.0.1:5000/


---

🖼 Screenshots

Homepage



Donation Form



Donors List




---

🔑 Example Code Snippets

HTML Donation Form (index.html)

<form action="/donate" method="POST">
  <input type="text" name="name" placeholder="Your Name" required>
  <input type="email" name="email" placeholder="Your Email" required>
  <input type="number" name="amount" placeholder="Donation Amount" required>
  <select name="cause">
    <option>Clean Water</option>
    <option>Food Support</option>
    <option>Education</option>
    <option>Healthcare</option>
  </select>
  <button type="submit">Proceed to Payment</button>
</form>

Flask Route (app.py)

@app.route("/donate", methods=["POST"])
def donate():
    name = request.form['name']
    email = request.form['email']
    amount = request.form['amount']
    cause = request.form['cause']

    # Save donor info (in-memory or DB)
    donors.append({"name": name, "amount": amount, "cause": cause})

    # Send email receipt (optional)
    send_email(email, name, amount, cause)

    return render_template("success.html", name=name, amount=amount, cause=cause)

Auto Email Function

def send_email(to, name, amount, cause):
    msg = Message("Thank You for Your Donation ❤",
                  sender="your_email@gmail.com",
                  recipients=[to])
    msg.body = f"""
    Hello {name},

    Thank you for donating ${amount} towards {cause}.
    Your kindness helps us bring clean water, food, and education to families in need.

    – W9 Donation Team
    """
    mail.send(msg)


---

📧 Email Receipt (Example)

Subject: Thank You for Your Donation ❤

Hello John,

Thank you for donating $50 towards Clean Water.
Your kindness helps us bring clean water, food, and education to families in need.

– W9 Donation Team


---

🛠 Future Improvements

✅ Stripe/Razorpay integration for real payments

✅ Admin dashboard for managing donations

✅ Donor leaderboard



---

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.


---

📜 License

This project is licensed under the MIT License.


---
