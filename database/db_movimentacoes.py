from database.db import conectar_db
import pytz
from datetime import datetime


def db_adicionar_movimentacao(pessoa_id, item_id, qtd, obs):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        # Definir o fuso horário (UTC-3)
        fuso_horario = pytz.timezone('America/Sao_Paulo')
        data_atual = datetime.now(fuso_horario)
        # Formatar a data para exibir como "DD/MM/YYYY HH:MM:SS"
        data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")

        query = """
        INSERT INTO movimentacoes (pessoa_id, item_id, quantidade, observacao, data)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (pessoa_id, item_id, qtd, obs, data_formatada))
        conn.commit()
        print("[DB] SUCESSO - Adicionar Movimentacao")

    except Exception as e:
        print("[DB] ERRO - Adicionar movimentação:", e)
    finally:
        conn.close()

# Função para buscar movimentações
def db_buscar_movimentacoes(filtro_pessoa=0, filtro_item=0):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        params = []
        query = """
        SELECT 
            m.id,
            p.nome AS pessoa_nome,
            i.nome AS item_nome,
            m.quantidade,
            m.observacao,
            m.data
        FROM movimentacoes m
        INNER JOIN pessoas p ON m.pessoa_id = p.id
        INNER JOIN itens i ON m.item_id = i.id
        WHERE 1=1
        """

        if int(filtro_pessoa) > 0:
            query += " AND m.pessoa_id = ?"
            params.append(filtro_pessoa)
        if int(filtro_item) > 0:
            query += " AND m.item_id = ?"
            params.append(filtro_item)

        query += " ORDER BY m.data DESC"
        
        cursor.execute(query, params)
        movimentacoes = cursor.fetchall()
        print("[DB] SUCESSO - Buscar movimentacoes")
        return movimentacoes
    except Exception as e:
        print("[DB] ERRO - Buscar movimentacoes:", e)
        return []
    finally:
        conn.close()