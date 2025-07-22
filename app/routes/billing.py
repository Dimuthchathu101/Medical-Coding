from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Claim
from sqlalchemy import func
from app import db
from app.models import Appointment
from datetime import datetime

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/dashboard')
@login_required
def dashboard():
    total_claims = Claim.query.count()
    total_billed = db.session.query(func.sum(Claim.amount)).scalar() or 0
    total_paid = db.session.query(func.sum(Claim.amount)).filter(Claim.status == 'paid').scalar() or 0
    status_counts = db.session.query(Claim.status, func.count(Claim.id)).group_by(Claim.status).all()
    upcoming_appointments = Appointment.query.filter(Appointment.date_time >= datetime.now(), Appointment.status == 'scheduled').order_by(Appointment.date_time.asc()).limit(5).all()
    return render_template('billing/dashboard.html',
        total_claims=total_claims,
        total_billed=total_billed,
        total_paid=total_paid,
        status_counts=status_counts,
        upcoming_appointments=upcoming_appointments
    )

# Add billing and payment routes here 