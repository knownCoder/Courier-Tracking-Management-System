from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# ---------------- APP SETUP ----------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courier.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 🔐 REQUIRED FOR SESSION LOGIN
app.secret_key = "courier_tracking_secret_123"

# ---------------- DB SETUP ----------------
db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tracking_id = db.Column(db.String(50), unique=True, nullable=False)
    sender_name = db.Column(db.String(100))
    receiver_name = db.Column(db.String(100))

    current_status = db.Column(db.String(50))
    current_location = db.Column(db.String(100))

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html")

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    shipments = Shipment.query.all()
    return render_template("admin.html", shipments=shipments)

# ---------------- LOGOUT ----------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

#------------------SHIPMENT TRACKING----------------
@app.route("/admin/add", methods=["GET", "POST"])
def add_shipment():
    if request.method == "POST":
        shipment = Shipment(
    tracking_id=request.form["tracking_id"],
    sender_name=request.form["sender"],
    receiver_name=request.form["receiver"],
    current_status=request.form["status"],
    current_location=request.form["location"]
)

        db.session.add(shipment)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_shipment.html")

#------------------UPDATE SHIPMENT----------------

@app.route("/admin/update/<int:id>", methods=["POST"])
def update_status(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    shipment = Shipment.query.get_or_404(id)

    shipment.current_status = request.form["status"]
    shipment.current_location = request.form["location"]

    db.session.commit()

    return redirect(url_for("admin_dashboard"))

#---------------- TRACKING ----------------

@app.route("/track", methods=["GET", "POST"])
def track_shipment():
    shipment = None

    if request.method == "POST":
        tracking_id = request.form["tracking_id"]
        shipment = Shipment.query.filter_by(
            tracking_id=tracking_id
        ).first()

    return render_template(
        "track.html",
        shipment=shipment
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)

