from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.user_model import get_user_by_email, create_user

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona para a home
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha')
        
        user = get_user_by_email(email)
        
        # Verifica se o usuário existe e se a senha (hash) coincide com a digitada
        if user and check_password_hash(user['senha'], senha):
            # Salva o ID e o status de admin na sessão do navegador
            session['user_id'] = user['id']
            session['nome'] = user['nome']
            session['is_admin'] = user['is_admin']
            
            flash(f"Bem-vindo de volta, caçador {user['nome']}!", "sucesso")
            return redirect(url_for('index'))
        else:
            flash("E-mail ou senha incorretos. Tente novamente.", "perigo")
            
    return render_template('login.html')

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Impede acesso à página de cadastro se já estiver logado
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Verifica se o e-mail já está cadastrado para evitar duplicidade
        if get_user_by_email(email):
            flash("Este e-mail já está sendo usado por outro membro da corporação.", "perigo")
        elif senha != confirmar_senha:
            flash("As senhas não coincidem!", "perigo")
        else:
            if create_user(nome, email, senha):
                flash("Sua conta foi criada com sucesso! Agora você pode entrar.", "sucesso")
                return redirect(url_for('auth.login'))
            else:
                flash("Houve um erro técnico ao criar sua conta.", "perigo")
                
    return render_template('cadastro.html')

@bp.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    flash("Você saiu da sua conta.")
    return redirect(url_for('index'))