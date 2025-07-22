# Medical Coding & Billing System (Flask)

A secure, modular, and extensible medical coding and billing platform built with Python and Flask. Designed for compliance, scalability, and integration with healthcare systems.

## Features (Initial Foundation)
- User authentication (RBAC)
- Patient registration
- Coding entry (ICD-10, CPT, modifiers)
- Audit logging
- Secure configuration

## Setup
1. Clone the repo
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (see `.env.example`)
5. Run the app:
   ```bash
   flask run
   ```

## Structure
- `app/` - Main application code (models, routes, services, utils)
- `migrations/` - Database migrations
- `tests/` - Unit and integration tests

## Security & Compliance
- HIPAA-ready foundation
- Encryption at rest & in transit
- Audit trails
- Role-based access control

## Next Steps
- Implement additional modules (claims, payment posting, analytics)
- Integrate with EHR/clearinghouse APIs
- Expand test coverage

## API & Web Endpoints

### Authentication & User
- `/auth/register` (GET, POST): Register a new user
- `/auth/login` (GET, POST): User login
- `/auth/logout` (GET): Logout
- `/auth/notifications` (GET): View user notifications

### Patients
- `/patients/` (GET): List/search/sort patients
- `/patients/add` (GET, POST): Add patient (admin/coder)
- `/patients/<patient_id>` (GET): View patient details
- `/patients/<patient_id>/edit` (GET, POST): Edit patient (admin/coder)
- `/patients/<patient_id>/delete` (POST): Delete patient (admin/coder)
- `/patients/<patient_id>/upload` (GET, POST): Upload patient document
- `/patients/documents/<doc_id>/download` (GET): Download patient document
- `/patients/<patient_id>/appointments` (GET): List appointments for patient
- `/patients/<patient_id>/appointments/add` (GET, POST): Schedule appointment
- `/patients/appointments/<appt_id>/edit` (GET, POST): Edit appointment
- `/patients/appointments/<appt_id>/cancel` (POST): Cancel appointment

### Claims & Billing
- `/claims/patient/<patient_id>/claims` (GET): List claims for patient
- `/claims/patient/<patient_id>/claims/add` (GET, POST): Add claim (admin/biller)
- `/claims/claims/<claim_id>/edit` (GET, POST): Edit claim (admin/biller)
- `/claims/claims/<claim_id>/invoice` (GET): Download claim invoice (PDF)
- `/billing/dashboard` (GET): Billing & claims analytics dashboard

### Coding (AJAX)
- `/coding/search/icd10?q=...` (GET): Search ICD-10 codes
- `/coding/search/cpt?q=...` (GET): Search CPT codes

### Home
- `/` (GET): Redirects to dashboard or login