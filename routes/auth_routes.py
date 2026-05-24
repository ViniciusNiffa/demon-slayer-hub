from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash
from models.user_model import create_user, get_user_by_email
import os
import uuid
from config import UPLOAD_FOLDER

bp = Blueprint('auth', __name__)

@bp.route('/check_email')
def check_email():
    email = request.args.get('email')
    user = get_user_by_email(email)
    return jsonify({'exists': bool(user)})

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        file = request.files.get('foto')

        if not nome or not email or not senha:
            flash('Por favor, preencha todos os campos obrigatórios.')
            return redirect(url_for('auth.register'))

        if get_user_by_email(email):
            flash('E-mail já cadastrado.')
            return redirect(url_for('auth.register'))
        
        filename = 'default.png'
        if file and file.filename != '':
            ext = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        create_user(nome,email,senha,filename)
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_by_email(request.form.get('email'))

        if user and check_password_hash(user['senha'], request.form.get('senha')):
            session['user_id'] = user['id']
            session['nome'] = user['nome']
            session['is_admin'] = bool(user['is_admin']) # Necessário para o decorator @admin_required

            if user['is_admin']:
                return redirect(url_for('admin.admin'))
            
            return redirect(url_for('user.perfil'))
        
        flash('E-mail ou senha incorretos.')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))