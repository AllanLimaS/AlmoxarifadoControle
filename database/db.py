import sqlite3
from datetime import datetime
import pytz

# Função para conectar ao banco de dados
def conectar_db():
    conn = sqlite3.connect("storage\\estoque.db")
    return conn

# Função para criar as tabelas
def criar_tabelas():
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

# Função para adicionar item
def db_adicionar_item(nome, quantidade):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO itens (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
    conn.commit()
    conn.close()

# Função para adicionar pessoa
def db_adicionar_pessoa(nome):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pessoas (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def db_adicionar_movimentacao(pessoa_id, item_id, quantidade):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        # Definir o fuso horário de Itajaí, Santa Catarina (UTC-3)
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
        conn.close()
    except sqlite3.Error as e:
        print("Erro ao cadastrar movimentação:", e)
    finally:
        conn.close()

# Função para buscar itens
def db_buscar_itens():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens")
    itens = cursor.fetchall()
    conn.close()
    return itens

# Função para buscar pessoas
def db_buscar_pessoas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()
    return pessoas

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

        return movimentacoes
    except sqlite3.Error as e:
        print("Erro ao buscar movimentações:", e)
        return []
    finally:
        conn.close()
    

# Função para deletar item
def db_deletar_item(item_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()



# Função para deletar pessoa
def db_deletar_pessoa(pessoa_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id = ?", (pessoa_id,))
    conn.commit()
    conn.close()
