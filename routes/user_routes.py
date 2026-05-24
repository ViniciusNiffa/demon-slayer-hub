from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user_model import get_user_by_id, update_user, get_fanarts_by_user
from utils.decorators import login_required
import os
import uuid
from config import UPLOAD_FOLDER

user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    user_id = session['user_id']

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        biografia = request.form.get('biografia')
        respiracao_tipo = request.form.get('respiracao_tipo')
        file = request.files.get('foto')

        user = get_user_by_id(user_id)

        filename = user['foto']

        if file and file.filename != '':
            ext = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        if update_user(user_id, nome, email, filename, biografia, respiracao_tipo):
            flash("Perfil atualizado com sucesso!")
        else:
            flash("Erro ao atualizar perfil.")
            
        return redirect(url_for('user.perfil'))

    # Tratamento da requisição GET: busca os dados para exibir no formulário/página
    user = get_user_by_id(user_id)
    fanarts = get_fanarts_by_user(user_id)
    return render_template('perfil.html', user=user, fanarts=fanarts)

@user_bp.route('/perfil/<int:user_id>')
def ver_perfil(user_id):
    # Permite ver o perfil de outros usuários
    user = get_user_by_id(user_id)
    if not user:
        flash("Usuário não encontrado.")
        return redirect(url_for('index'))
    
    fanarts = get_fanarts_by_user(user_id)
    return render_template('perfil.html', user=user, fanarts=fanarts)