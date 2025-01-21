import sqlite3
import os

def verificar_ou_criar_pasta():
    pasta = "storage"

    # Verificar se a pasta já existe
    if not os.path.exists(pasta):
        # Se não existir, cria a pasta
        os.makedirs(pasta)
        print(f"A pasta '{pasta}' foi criada.")
    else:
        print(f"A pasta '{pasta}' já existe.")

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

    verificar_ou_criar_pasta()
    
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        # Criar tabela de usuário para login 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
        """)
        
        
        # Criar tabela de itens
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            entrada INTEGER NOT NULL,
            saida INTEGER NOT NULL
                       
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
            observacao TEXT DEFAULT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas (id),
            FOREIGN KEY (item_id) REFERENCES itens (id)
        );
        """)

        conn.commit()
        conn.close()    
    except sqlite3.Error as e:
        print(f"[DB] ERRO - Criar tabelas no banco de dados: {e}")








    

