import csv
import sys
from app import create_app, db
from app.models import ICD10Code, CPTCode

"""
Usage:
  python import_codes.py icd10 path/to/icd10.csv
  python import_codes.py cpt path/to/cpt.csv

CSV format:
  ICD-10: code,description,category
  CPT: code,description,category
"""

def import_icd10(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['code', 'description', 'category'])
        for row in reader:
            if not ICD10Code.query.filter_by(code=row['code']).first():
                db.session.add(ICD10Code(code=row['code'], description=row['description'], category=row['category']))
        db.session.commit()
    print('ICD-10 codes imported.')

def import_cpt(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['code', 'description', 'category'])
        for row in reader:
            if not CPTCode.query.filter_by(code=row['code']).first():
                db.session.add(CPTCode(code=row['code'], description=row['description'], category=row['category']))
        db.session.commit()
    print('CPT codes imported.')

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in ('icd10', 'cpt'):
        print(__doc__)
        sys.exit(1)
    app = create_app()
    with app.app_context():
        if sys.argv[1] == 'icd10':
            import_icd10(sys.argv[2])
        else:
            import_cpt(sys.argv[2]) 