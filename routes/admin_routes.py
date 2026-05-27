from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import get_all_users, get_user_by_id, update_user, delete_user, create_user, get_user_by_email
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

    if search:
        users = [user for user in users if search in user['nome'].lower() or search in user['email'].lower()]

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
            flash("Erro ao atualizar usuário.", "perigo")

        return redirect(url_for('admin.admin'))
    
    return render_template('edit_user.html', user=user)

@admin_bp.route('/admin/delete/<int:user_id>')
@admin_required
def delete(user_id):
    if session.get('user_id') == user_id:
        flash("Erro: Você não pode deletar sua própria conta administrativa.", "perigo")
        return redirect(url_for('admin.admin'))
    
    if delete_user(user_id):
        flash("Usuário removido com sucesso.", "sucesso")
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/create_user', methods=['GET', 'POST'])
@admin_required
def create_user_admin():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        # O checkbox retorna '1' se marcado, caso contrário, não é enviado no request.form
        is_admin = 1 if request.form.get('is_admin') else 0

        if not nome or not email or not senha or not confirmar_senha:
            flash("Todos os campos são obrigatórios.", "perigo")
            return render_template('admin_create_user.html')

        if get_user_by_email(email):
            flash("Este e-mail já está sendo usado por outro membro da corporação.", "perigo")
            return render_template('admin_create_user.html')
        
        if senha != confirmar_senha:
            flash("As senhas não coincidem!", "perigo")
            return render_template('admin_create_user.html')
        
        if create_user(nome, email, senha, is_admin=is_admin):
            flash(f"Usuário '{nome}' criado com sucesso!", "sucesso")
            return redirect(url_for('admin.admin'))
        else:
            flash("Houve um erro técnico ao criar o usuário.", "perigo")

    return render_template('admin_create_user.html')