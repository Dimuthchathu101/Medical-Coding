from flask import Blueprint, request, jsonify
from app.models import ICD10Code, CPTCode

coding_bp = Blueprint('coding', __name__)

@coding_bp.route('/search/icd10')
def search_icd10():
    q = request.args.get('q', '').strip()
    results = []
    if q:
        codes = ICD10Code.query.filter(
            (ICD10Code.code.ilike(f'%{q}%')) | (ICD10Code.description.ilike(f'%{q}%'))
        ).limit(20).all()
        results = [{
            'id': code.id,
            'code': code.code,
            'description': code.description
        } for code in codes]
    return jsonify(results)

@coding_bp.route('/search/cpt')
def search_cpt():
    q = request.args.get('q', '').strip()
    results = []
    if q:
        codes = CPTCode.query.filter(
            (CPTCode.code.ilike(f'%{q}%')) | (CPTCode.description.ilike(f'%{q}%'))
        ).limit(20).all()
        results = [{
            'id': code.id,
            'code': code.code,
            'description': code.description
        } for code in codes]
    return jsonify(results) 