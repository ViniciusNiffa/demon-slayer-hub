from database import get_connection
from config import DEFAULT_IMAGE
from werkzeug.security import generate_password_hash

def create_user(nome, email, senha, foto=DEFAULT_IMAGE):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Criptografamos aqui para garantir que NENHUM usuário seja criado sem hash
        hashed_password = generate_password_hash(senha)
        cursor.execute(
            """INSERT INTO users (nome, email, senha, foto) VALUES (?, ?, ?, ?)""",
            (nome, email, hashed_password, foto)
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

        
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Erro ao buscar usuário por email: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Erro ao buscar usuário por ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_by_nome(nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE nome = ?', (nome,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Erro ao buscar usuário por nome: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_user(user_id, nome, email, foto, biografia, respiracao_tipo):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE users SET nome = ?, email = ?, foto = ?, biografia = ?, respiracao_tipo = ? WHERE id = ?',
            (nome, email, foto, biografia, respiracao_tipo, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()   

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def follow_user(seguidor_id, seguido_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO seguidores (seguidor_id, seguido_id) VALUES (?, ?)', (seguidor_id, seguido_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao seguir usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_followers(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM seguidores WHERE seguido_id = ?', (user_id,))
        followers = cursor.fetchall()
        return followers
    except Exception as e:
        print(f"Erro ao obter seguidores: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_following(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM seguidores WHERE seguidor_id = ?', (user_id,))
        following = cursor.fetchall()
        return following
    except Exception as e:
        print(f"Erro ao obter seguindo: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def unfollow_user(seguidor_id, seguido_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM seguidores WHERE seguidor_id = ? AND seguido_id = ?', (seguidor_id, seguido_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deixar de seguir usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def create_denuncia(user_id, fanart_id, motivo):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO denuncias (user_id, fanart_id, motivo) VALUES (?, ?, ?)',
            (user_id, fanart_id, motivo)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao criar denúncia: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def like_fanart(user_id, fanart_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Usamos INSERT OR IGNORE para evitar que o mesmo usuário curta várias vezes
        cursor.execute(
            'INSERT INTO likes (user_id, fanart_id) VALUES (?, ?)',
            (user_id, fanart_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao curtir fanart: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def unlike_fanart(user_id, fanart_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM likes WHERE user_id = ? AND fanart_id = ?',
            (user_id, fanart_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao descurtir fanart: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def has_user_liked(user_id, fanart_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT 1 FROM likes WHERE user_id = ? AND fanart_id = ?', (user_id, fanart_id))
        return cursor.fetchone() is not None
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()

def get_fanarts_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM fanarts WHERE user_id = ?', (user_id,))
        fanarts = cursor.fetchall()
        return fanarts
    except Exception as e:
        print(f"Erro ao obter fanarts: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_fanart_by_id(fanart_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT f.*, u.nome AS autor_nome, u.foto AS autor_foto 
            FROM fanarts f 
            JOIN users u ON f.user_id = u.id 
            WHERE f.id = ?''', (fanart_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter fanart por ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def create_fanart(user_id, titulo, descricao, imagem, categoria):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO fanarts (user_id, titulo, descricao, imagem, categoria) VALUES (?, ?, ?, ?, ?)',
            (user_id, titulo, descricao, imagem, categoria)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao criar fanart: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def search_fanarts(titulo=None, categoria=None, ordem='recentes', user_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Selecionamos fanarts, o nome do autor, total de likes e se o usuário logado curtiu
        sql = """
            SELECT f.*, u.nome AS autor_nome, COUNT(l.id) AS total_likes,
            (SELECT 1 FROM likes WHERE fanart_id = f.id AND user_id = ?) AS curtiu
            FROM fanarts f
            JOIN users u ON f.user_id = u.id
            LEFT JOIN likes l ON f.id = l.fanart_id
            WHERE 1=1
        """
        params = [user_id]
        
        if titulo:
            sql += " AND f.titulo LIKE ?"
            params.append(f"%{titulo}%")
        
        if categoria:
            sql += " AND f.categoria = ?"
            params.append(categoria)
            
        sql += " GROUP BY f.id"

        if ordem == 'curtidas':
            sql += " ORDER BY total_likes DESC, f.created_at DESC"
        else:
            sql += " ORDER BY f.created_at DESC"
            
        cursor.execute(sql, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao pesquisar fanarts: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_fanart(user_id, fanart_id, titulo, descricao, imagem, categoria):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE fanarts SET titulo = ?, descricao = ?, imagem = ?, categoria = ? WHERE id = ? AND user_id = ?',
            (titulo, descricao, imagem, categoria, fanart_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar fanart: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_fanart(user_id, fanart_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM fanarts WHERE user_id = ? AND id = ?', (user_id, fanart_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar fanart: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def create_comentario(user_id, fanart_id, comentario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO comentarios (user_id, fanart_id, comentario) VALUES (?, ?, ?)', (user_id, fanart_id, comentario))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao publicar comentário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
    
def update_comentario(comentario_id, novo_comentario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE comentarios SET comentario = ? WHERE id = ?', (novo_comentario, comentario_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao editar comentário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_comentario(comentario_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM comentarios WHERE id = ?', (comentario_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar comentário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_comentarios_by_fanart(fanart_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Buscamos o comentário e o nome de quem comentou (usando JOIN)
        cursor.execute('''
            SELECT c.*, u.nome 
            FROM comentarios c
            JOIN users u ON c.user_id = u.id
            WHERE c.fanart_id = ?
            ORDER BY c.created_at DESC
        ''', (fanart_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()