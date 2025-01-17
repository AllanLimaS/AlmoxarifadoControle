from database.db import conectar_db

# Função para adicionar pessoa
def db_adicionar_pessoa(nome):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pessoas (nome) VALUES (?)", (nome,))
        conn.commit()
        print("[DB] SUCESSO - Adicionar Pessoa")
    except Exception as e:
        print(f"[DB] ERRO - Adicionar Pessoa: {e}")
    finally:
        conn.close()


# Função para buscar pessoas
def db_buscar_pessoas():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pessoas")
        pessoas = cursor.fetchall()
        print("[DB] SUCESSO - Buscar Pessoas")
        return pessoas
    except Exception as e:
        print(f"[DB] ERRO - Buscar Pessoas: {e}")
        return [] 
    finally: 
        conn.close()

# Função para deletar pessoa
def db_deletar_pessoa(pessoa_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pessoas WHERE id = ?", (pessoa_id,))
        conn.commit()
        print("[DB] SUCESSO - Deletar Pessoa")
    except Exception as e:
        print("[DB] ERRO - Deletar Pessoa:", e)
    finally:
        conn.close()