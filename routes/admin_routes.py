from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import get_all_users, get_user_by_id, get_user_by_nome, create_user, update_user, delete_user
from utils.decorators import admin_required
import os
import uuid
from config import UPLOAD_FOLDER

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_required
def admin():
    search = request.args.get('search','').lower()
    order = request.args.get('order','nome')
    page = int(request.args.get('page', 1))
    per_page = 10

    users = get_all_users()

    # Filtro de busca
    if search:
        users = [user for user in users if search in user['nome'].lower() or search in user['email'].lower()]

    # Ordenação segura: verifica se a chave de ordenação existe nos dados
    if users and order in users[0].keys():
        users = sorted(users, key=lambda x: x[order])

    total_users = len(users)
    total_pages = (total_users + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    users_paginated = users[start:end]

    return render_template('admin.html', users=users_paginated, total=total_users, 
                           total_pages=total_pages, page=page, search=search, order=order)

@admin_bp.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        biografia = request.form.get('biografia')
        file = request.files.get('foto')
        respiracao_tipo = request.form.get('respiracao_tipo')

        filename = user['foto']

        if file and file.filename != '':
            ext = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        if update_user(user_id, nome, email, filename, biografia, respiracao_tipo):
            flash("Usuário atualizado com sucesso!", "sucesso")
        else:
            flash("Erro ao atualizar usuário.", "erro")

        return redirect(url_for('admin.admin'))
    
    return render_template('edit_user.html', user=user)

@admin_bp.route('/admin/delete/<int:user_id>')
@admin_required
def delete(user_id):
    # Proteção: impede que o admin delete a própria conta logada
    if session.get('user_id') == user_id:
        flash("Erro: Você não pode deletar sua própria conta administrativa.", "erro")
        return redirect(url_for('admin.admin'))
    
    if delete_user(user_id):
        flash("Usuário removido com sucesso.", "sucesso")
    return redirect(url_for('admin.admin'))