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