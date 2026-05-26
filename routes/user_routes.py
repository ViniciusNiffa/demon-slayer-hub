from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user_model import get_user_by_id, update_user, get_fanarts_by_user, create_fanart
from utils.decorators import login_required
import os
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER

user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil', methods=['GET', 'POST'])
@user_bp.route('/perfil/<int:user_id>', methods=['GET', 'POST'])
@login_required
def perfil(user_id=None):
    target_id = user_id if user_id else session.get('user_id')
    user = get_user_by_id(target_id)
    
    if not user:
        flash("Caçador não encontrado!")
        return redirect(url_for('index'))

    if session.get('user_id') == target_id:
        session['user_foto'] = user['foto']

    if request.method == 'POST' and session.get('user_id') == target_id:
        nome = request.form.get('nome')
        email = request.form.get('email')
        biografia = request.form.get('biografia', '').strip()
        respiracao = user['respiracao_tipo']
        foto = user['foto']

        file = request.files.get('foto')
        if file and file.filename != '':
            filename = secure_filename(f"user_{target_id}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            foto = filename

        update_user(target_id, nome, email, foto, biografia, respiracao)
        session['user_foto'] = foto
        flash("Perfil atualizado com sucesso!")
        return redirect(url_for('user.perfil'))

    fanarts = get_fanarts_by_user(target_id, session.get('user_id'))
    return render_template('perfil.html', user=user, fanarts=fanarts)

@user_bp.route('/perfil/remover-foto', methods=['POST'])
@login_required
def remover_foto():
    target_id = session.get('user_id')
    user = get_user_by_id(target_id)
    if user:
        foto_padrao = 'pastaBanner/default.png'
        update_user(target_id, user['nome'], user['email'], foto_padrao, user['biografia'] or '', user['respiracao_tipo'] or '')
        session['user_foto'] = foto_padrao
        flash("Sua foto de perfil foi removida com sucesso!", "sucesso")
    return redirect(url_for('user.perfil'))

@user_bp.route('/fanart/enviar', methods=['GET', 'POST'])
@login_required
def enviar_fanart():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao', '')
        categoria = request.form.get('categoria', 'Outros')
        file = request.files.get('imagem')

        if not titulo or not file or file.filename == '':
            flash("Título e imagem são obrigatórios!", "perigo")
            return redirect(request.url)

        filename = secure_filename(f"fanart_{session['user_id']}_{file.filename}")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        create_fanart(session['user_id'], titulo, descricao, filename, categoria)
        flash("Fanart enviada com sucesso! Ela aparecerá no seu perfil.", "sucesso")
        return redirect(url_for('user.perfil'))

    return render_template('enviar_fanart.html')