import hashlib

from database.db import conectar_db

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Verificar se existe usuário
def db_usuario_existe():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario")
        existe = cursor.fetchone()[0] > 0
        print("[DB] SUCESSO - Verifica Usuario existe")
        return existe
    except Exception as e:
        print(f"[DB] ERRO - Verifica Usuario existe: {e}")
        return [] 
    finally: 
        conn.close()

# Função para adicionar usuário
def db_adicionar_usuario(login,senha):
    try:
        senha_hashed = hash_senha(senha)

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario (login, senha) VALUES (?,?)", (login, senha_hashed))
        conn.commit()
        print("[DB] SUCESSO - Adicionar Usuario")
    except Exception as e:
        print(f"[DB] ERRO -  Adicionar Usuario: {e}")
    finally:
        conn.close()

# Função para buscar usuário
def db_buscar_usuario():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuario = cursor.fetchall()
        print("[DB] SUCESSO - Buscar Usuario")
        return usuario
    except Exception as e:
        print(f"[DB] ERRO - Buscar Usuario: {e}")
        return [] 
    finally: 
        conn.close()

# Função para autenticar
def db_autenticar(login,senha):
    try:
        senha_hashed = hash_senha(senha)

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM usuario WHERE login = ? AND senha = ?",
        (login, senha_hashed),
        )

        usuario = cursor.fetchone()

        print("[DB] SUCESSO - Autenticar Login")
        
        if usuario:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"[DB] ERRO -  Autenticar Login: {e}")
    finally:
        conn.close()