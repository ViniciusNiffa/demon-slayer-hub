from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import create_fanart, get_fanart_by_id, create_comentario, like_fanart, unlike_fanart, has_user_liked, get_comentarios_by_fanart, search_fanarts
from utils.decorators import login_required
import os
import uuid
from config import UPLOAD_FOLDER

fanart_bp = Blueprint('fanart', __name__)

@fanart_bp.route('/fanart/nova', methods=['GET', 'POST'])
@login_required
def nova_fanart():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        categoria = request.form.get('categoria')
        file = request.files.get('imagem')
        user_id = session['user_id']

        if not titulo or not categoria or not file:
            flash("Título, categoria e imagem são obrigatórios.")
            return redirect(url_for('fanart.nova_fanart'))

        # Gerando nome único para a imagem
        ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        if create_fanart(user_id, titulo, descricao, filename, categoria):
            flash("Fanart publicada com sucesso!")
            return redirect(url_for('index'))
        else:
            flash("Erro ao publicar fanart.")

    return render_template('nova_fanart.html')

@fanart_bp.route('/fanarts')
def fanarts():
    fanarts_list = search_fanarts()
    return render_template('index.html', fanarts=fanarts_list)

@fanart_bp.route('/fanart/<int:fanart_id>')
def ver_fanart(fanart_id):
    fanart = get_fanart_by_id(fanart_id)
    if not fanart:
        flash("Fanart não encontrada.")
        return redirect(url_for('index'))
    
    comentarios = get_comentarios_by_fanart(fanart_id)
    curtiu = False
    if 'user_id' in session:
        curtiu = has_user_liked(session['user_id'], fanart_id)

    return render_template('ver_fanart.html', fanart=fanart, curtiu=curtiu, comentarios=comentarios)

@fanart_bp.route('/fanart/<int:fanart_id>/like', methods=['POST'])
@login_required
def curtir(fanart_id):
    user_id = session['user_id']
    if has_user_liked(user_id, fanart_id):
        unlike_fanart(user_id, fanart_id)
    else:
        like_fanart(user_id, fanart_id)
    return redirect(url_for('fanart.ver_fanart', fanart_id=fanart_id))

@fanart_bp.route('/fanart/<int:fanart_id>/comentar', methods=['POST'])
@login_required
def comentar(fanart_id):
    user_id = session['user_id']
    texto = request.form.get('comentario')
    
    if texto:
        create_comentario(user_id, fanart_id, texto)
        flash("Comentário enviado!")
    
    return redirect(url_for('fanart.ver_fanart', fanart_id=fanart_id))