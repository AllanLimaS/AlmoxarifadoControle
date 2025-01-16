import sqlite3

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
def db_adicionar_pessoa(nome, email):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pessoas (nome) VALUES (?)", (nome))
    conn.commit()
    conn.close()

# Função para buscar itens
def db_buscar_itens():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens")
    itens = cursor.fetchall()
    conn.close()
    return itens

# Função para deletar item
def db_deletar_item(item_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# Função para buscar pessoas
def db_buscar_pessoas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()
    return pessoas
