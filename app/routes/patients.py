from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Patient, db
from app.utils.security import roles_required
import os
from flask import send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.models import PatientDocument
from app.utils.compliance import log_audit

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

patients_bp = Blueprint('patients', __name__)

# Add patient registration and management routes here 

@patients_bp.route('/')
@login_required
def list_patients():
    query = Patient.query.filter_by(created_by=current_user.id)
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'last_name')
    order = request.args.get('order', 'asc')
    if search:
        query = query.filter(
            (Patient.first_name.ilike(f'%{search}%')) |
            (Patient.last_name.ilike(f'%{search}%'))
        )
    if sort in ['first_name', 'last_name', 'dob']:
        sort_col = getattr(Patient, sort)
        if order == 'desc':
            sort_col = sort_col.desc()
        else:
            sort_col = sort_col.asc()
        query = query.order_by(sort_col)
    patients = query.all()
    return render_template('patients/list.html', patients=patients, search=search, sort=sort, order=order)

@patients_bp.route('/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'coder')
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        insurance = request.form['insurance']
        patient = Patient(first_name=first_name, last_name=last_name, dob=dob, insurance=insurance, created_by=current_user.id)
        db.session.add(patient)
        db.session.commit()
        log_audit('add', 'Patient', patient.id, f'Added patient {patient.first_name} {patient.last_name}')
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
@roles_required('admin', 'coder')
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
        log_audit('edit', 'Patient', patient.id, f'Edited patient {patient.first_name} {patient.last_name}')
        flash('Patient updated successfully.')
        return redirect(url_for('patients.view_patient', patient_id=patient.id))
    return render_template('patients/edit.html', patient=patient)

@patients_bp.route('/<int:patient_id>/delete', methods=['POST'])
@login_required
@roles_required('admin', 'coder')
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.created_by != current_user.id:
        flash('Access denied.')
        return redirect(url_for('patients.list_patients'))
    db.session.delete(patient)
    db.session.commit()
    log_audit('delete', 'Patient', patient.id, f'Deleted patient {patient.first_name} {patient.last_name}')
    flash('Patient deleted successfully.')
    return redirect(url_for('patients.list_patients')) 

@patients_bp.route('/<int:patient_id>/upload', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'coder')
def upload_document(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.created_by != current_user.id and current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('patients.view_patient', patient_id=patient_id))
    if request.method == 'POST':
        file = request.files.get('document')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            doc = PatientDocument(filename=filename, filepath=filepath, patient_id=patient.id)
            db.session.add(doc)
            db.session.commit()
            log_audit('upload', 'PatientDocument', doc.id, f'Uploaded document {filename} for patient {patient.id}')
            flash('Document uploaded successfully.')
            return redirect(url_for('patients.view_patient', patient_id=patient.id))
        flash('No file selected.')
    return render_template('patients/upload.html', patient=patient)

@patients_bp.route('/documents/<int:doc_id>/download')
@login_required
def download_document(doc_id):
    doc = PatientDocument.query.get_or_404(doc_id)
    patient = Patient.query.get(doc.patient_id)
    if patient.created_by != current_user.id and current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('patients.view_patient', patient_id=patient.id))
    directory = os.path.dirname(doc.filepath)
    return send_from_directory(directory, doc.filename, as_attachment=True) 