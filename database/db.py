import sqlite3
from datetime import datetime
import pytz

# Função para conectar ao banco de dados
def conectar_db():
    try:
        conn = sqlite3.connect("storage\\estoque.db")
        return conn
    except sqlite3.Error as e:
        print(f"[DB] ERRO - Conectar ao banco de dados: {e}")
        return None  # Retorna None em caso de erro de conexão


# Função para criar as tabelas
def criar_tabelas():
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        # Criar tabela de itens
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        );
        """)

        # Criar tabela de pessoas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        );
        """)

        # Criar tabela de movimentações
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pessoa_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas (id),
            FOREIGN KEY (item_id) REFERENCES itens (id)
        );
        """)

        conn.commit()
        conn.close()    
    except sqlite3.Error as e:
        print(f"[DB] ERRO - Criar tabelas no banco de dados: {e}")

# Função para adicionar item
def db_adicionar_item(nome, quantidade):
    try:
        conn = conectar_db()
        cursor  = conn.cursor()
        cursor.execute("INSERT INTO itens (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        conn.commit()
        print("[DB] SUCESSO - Adicionar Item")
    except Exception as e:
        print(f"[DB] ERRO - Adicionar item: {e}")
    finally:
        conn.close()

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

def db_adicionar_movimentacao(pessoa_id, item_id, quantidade):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        # Definir o fuso horário (UTC-3)
        fuso_horario = pytz.timezone('America/Sao_Paulo')
        data_atual = datetime.now(fuso_horario)
        # Formatar a data para exibir como "DD/MM/YYYY HH:MM:SS"
        data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")

        query = """
        INSERT INTO movimentacoes (pessoa_id, item_id, quantidade, data)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (pessoa_id, item_id, quantidade, data_formatada))
        conn.commit()
        print("[DB] SUCESSO - Adicionar Movimentacao")

    except Exception as e:
        print("[DB] ERRO - Adicionar movimentação:", e)
    finally:
        conn.close()

# Função para buscar itens
def db_buscar_itens():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itens")
        itens = cursor.fetchall()
        print("[DB] SUCESSO - Buscar Itens")
        return itens
    except Exception as e:
        print("[DB] ERRO - Buscar itens:", e)
        return []
    finally:
        conn.close()

# Função para buscar item
def db_buscar_item(item_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itens WHERE id = ?",(item_id,))
        itens = cursor.fetchall()
        print("[DB] SUCESSO - Buscar Item")
        return itens
    except Exception as e:
        print("[DB] ERRO - Buscar item:", e)
        return []
    finally:
        conn.close()
        

def db_diminuir_saldo_item(item_id, qtd):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE itens SET quantidade = quantidade - ? WHERE id = ? AND quantidade >= ?",
            (qtd, item_id, qtd)
        )
        if cursor.rowcount == 0:
            raise ValueError("Quantidade insuficiente para o item ou item não encontrado.")
        conn.commit()
        print("[DB] SUCESSO - Diminuir Saldo Item")

    except Exception as e:
        print(f"[DB] ERRO - Diminuir Saldo Item: {e}")
        conn.rollback()
    finally:
        conn.close()

def db_alterar_saldo_item(item_id, qtd):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE itens SET quantidade = ? WHERE id = ?",
            (qtd, item_id)
        )
        conn.commit()
        print("[DB] SUCESSO - Alterar Saldo Item")

    except Exception as e:
        print(f"[DB] ERRO - Alterar Saldo Item: {e}")
        conn.rollback()
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
    

# Função para buscar movimentações
def db_buscar_movimentacoes():
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        query = """
        SELECT 
            m.id,
            p.nome AS pessoa_nome,
            i.nome AS item_nome,
            m.quantidade,
            m.data
        FROM movimentacoes m
        INNER JOIN pessoas p ON m.pessoa_id = p.id
        INNER JOIN itens i ON m.item_id = i.id
        ORDER BY m.data DESC
        """
        cursor.execute(query)
        movimentacoes = cursor.fetchall()
        print("[DB] SUCESSO - Buscar movimentacoes")
        return movimentacoes
    except Exception as e:
        print("[DB] ERRO - Buscar movimentacoes:", e)
        return []
    finally:
        conn.close()
    

# Função para deletar item
def db_deletar_item(item_id):
    try: 
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM itens WHERE id = ?", (item_id,))
        conn.commit()
        print("[DB] SUCESSO - Deletar item")
    except Exception as e:
        print("[DB] ERRO - Deletar item:", e)
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
