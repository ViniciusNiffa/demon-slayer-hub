from flask import Flask, render_template, request, session
from database import init_db
from routes.auth_routes import bp as auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.fanart_routes import fanart_bp
from models.quiz_routes import quiz_bp
from models.user_model import search_fanarts

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)

with app.app_context():
    init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(fanart_bp)
app.register_blueprint(quiz_bp)

@app.route('/')
def index():
    titulo = request.args.get('titulo')
    categoria = request.args.get('categoria')
    ordem = request.args.get('ordem', 'recentes')
    user_id = session.get('user_id')

    fanarts = search_fanarts(titulo=titulo, categoria=categoria, ordem=ordem, user_id=user_id, limit=4)
    return render_template('index.html', fanarts=fanarts, ordem=ordem)

@app.route('/arcos')
def arcos():
    return render_template('pages/arcos.html')

@app.route('/personagens')
def personagens():
    return render_template('pages/mundo/personagens.html')

@app.route('/respiracoes')
def respiracoes():
    return render_template('pages/mundo/respiracoes.html')

@app.route('/mangas')
def mangas():
    return render_template('pages/mangas.html')

@app.route('/mundo')
def mundo():
    return render_template('pages/mundo.html')
if __name__ == '__main__':
    app.run(debug=True)