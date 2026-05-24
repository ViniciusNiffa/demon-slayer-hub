from flask import Blueprint, render_template, request, jsonify, session
from models.user_model import update_user_respiracao

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/descubra')
def descubra():
    return render_template('descubra_respiracao.html')

@quiz_bp.route('/descubra/salvar', methods=['POST'])
def salvar_respiracao():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Faça login para salvar seu resultado'}), 401
    
    data = request.get_json()
    respiracao = data.get('respiracao')
    user_id = session.get('user_id')
    
    if update_user_respiracao(user_id, respiracao):
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Erro ao salvar no banco de dados'}), 500