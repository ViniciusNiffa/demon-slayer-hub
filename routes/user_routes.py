from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user_model import get_user_by_id, update_user, get_fanarts_by_user
from utils.decorators import login_required
import os
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER

user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil')
@user_bp.route('/perfil/<int:user_id>')
@login_required
def perfil(user_id=None):
    # Se não for passado um ID, mostra o perfil do usuário logado
    target_id = user_id if user_id else session.get('user_id')
    user = get_user_by_id(target_id)
    
    if not user:
        flash("Caçador não encontrado!")
        return redirect(url_for('index'))

    if request.method == 'POST' and session.get('user_id') == target_id:
        nome = request.form.get('nome')
        email = request.form.get('email')
        biografia = request.form.get('biografia')
        respiracao = user['respiracao_tipo']
        foto = user['foto']

        # Logica simples para upload de foto se houver
        file = request.files.get('foto')
        if file and file.filename != '':
            filename = secure_filename(f"user_{target_id}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            foto = filename

        update_user(target_id, nome, email, foto, biografia, respiracao)
        flash("Perfil atualizado com sucesso!")
        return redirect(url_for('user.perfil'))

    fanarts = get_fanarts_by_user(target_id)
    return render_template('perfil.html', user=user, fanarts=fanarts)