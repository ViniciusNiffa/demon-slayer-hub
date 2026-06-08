from flask import Blueprint, render_template, request, session, jsonify
from models.user_model import update_user_respiracao

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/descubra')
def descubra():
    return render_template('descubra.html')

@quiz_bp.route('/descubra/salvar', methods=['POST'])
def salvar_respiracao():
    # Verifica se o usuário está logado para salvar o resultado
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    data = request.get_json()
    if not data or 'respiracao' not in data:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    respiracao = data.get('respiracao')
    user_id = session.get('user_id')

    if update_user_respiracao(user_id, respiracao):
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Error saving to database'}), 500