from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica se o id do usuário está na sessão (logado)
        if 'user_id' not in session:
            flash("Você precisa estar logado para acessar esta página.")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica se o usuário logado tem privilégios de admin
        if not session.get('is_admin'):
            flash("Acesso restrito a administradores.")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function