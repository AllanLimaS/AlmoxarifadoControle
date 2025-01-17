from database.db import conectar_db

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