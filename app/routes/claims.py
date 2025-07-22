from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Claim, Patient, db, Notification
from app.utils.security import roles_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
import io
from app.utils.compliance import log_audit

claims_bp = Blueprint('claims', __name__)

@claims_bp.route('/patient/<int:patient_id>/claims')
@login_required
def list_claims(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    claims = Claim.query.filter_by(patient_id=patient.id).all()
    return render_template('claims/list.html', patient=patient, claims=claims)

@claims_bp.route('/patient/<int:patient_id>/claims/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'biller')
def add_claim(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        amount = request.form['amount']
        status = request.form.get('status', 'pending')
        claim = Claim(patient_id=patient.id, amount=amount, status=status)
        db.session.add(claim)
        db.session.commit()
        log_audit('add', 'Claim', claim.id, f'Added claim for patient {patient.id}, amount ${amount}, status {status}')
        flash('Claim created successfully.')
        return redirect(url_for('claims.list_claims', patient_id=patient.id))
    return render_template('claims/add.html', patient=patient)

@claims_bp.route('/claims/<int:claim_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'biller')
def edit_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    if request.method == 'POST':
        claim.amount = request.form['amount']
        old_status = claim.status
        claim.status = request.form['status']
        db.session.commit()
        log_audit('edit', 'Claim', claim.id, f'Edited claim {claim.id}, amount ${claim.amount}, status {claim.status}')
        # Notify patient creator if status changed
        if claim.status != old_status:
            patient = claim.patient
            message = f'Claim #{claim.id} for {patient.first_name} {patient.last_name} status changed to {claim.status}.'
            notification = Notification(user_id=patient.created_by, message=message)
            db.session.add(notification)
            db.session.commit()
        flash('Claim updated successfully.')
        return redirect(url_for('claims.list_claims', patient_id=claim.patient_id))
    return render_template('claims/edit.html', claim=claim)

@claims_bp.route('/claims/<int:claim_id>/invoice')
@login_required
def download_invoice(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    patient = claim.patient
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont('Helvetica', 14)
    p.drawString(100, 750, f"Invoice for Claim #{claim.id}")
    p.setFont('Helvetica', 12)
    p.drawString(100, 720, f"Patient: {patient.first_name} {patient.last_name}")
    p.drawString(100, 700, f"Date of Birth: {patient.dob}")
    p.drawString(100, 680, f"Claim Amount: ${claim.amount:.2f}")
    p.drawString(100, 660, f"Status: {claim.status}")
    p.drawString(100, 640, f"Created: {claim.created_at}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"invoice_claim_{claim.id}.pdf", mimetype='application/pdf') 