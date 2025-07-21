from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Patient, db

patients_bp = Blueprint('patients', __name__)

# Add patient registration and management routes here 

@patients_bp.route('/')
@login_required
def list_patients():
    patients = Patient.query.filter_by(created_by=current_user.id).all()
    return render_template('patients/list.html', patients=patients)

@patients_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        insurance = request.form['insurance']
        patient = Patient(first_name=first_name, last_name=last_name, dob=dob, insurance=insurance, created_by=current_user.id)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully.')
        return redirect(url_for('patients.list_patients'))
    return render_template('patients/add.html')

@patients_bp.route('/<int:patient_id>')
@login_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.created_by != current_user.id:
        flash('Access denied.')
        return redirect(url_for('patients.list_patients'))
    return render_template('patients/view.html', patient=patient)

@patients_bp.route('/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.created_by != current_user.id:
        flash('Access denied.')
        return redirect(url_for('patients.list_patients'))
    if request.method == 'POST':
        patient.first_name = request.form['first_name']
        patient.last_name = request.form['last_name']
        patient.dob = request.form['dob']
        patient.insurance = request.form['insurance']
        db.session.commit()
        flash('Patient updated successfully.')
        return redirect(url_for('patients.view_patient', patient_id=patient.id))
    return render_template('patients/edit.html', patient=patient)

@patients_bp.route('/<int:patient_id>/delete', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.created_by != current_user.id:
        flash('Access denied.')
        return redirect(url_for('patients.list_patients'))
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully.')
    return redirect(url_for('patients.list_patients')) 