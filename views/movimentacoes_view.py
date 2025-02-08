import flet as ft

from database.db_movimentacoes import *
from database.db_itens import db_buscar_itens,db_buscar_item,db_diminuir_saldo_item,db_retornar_saldo_item
from database.db_pessoas import db_buscar_pessoas

alert = ft.AlertDialog(title=ft.Text("Movimento Cadastrado com Sucesso!"))

def show_alert(e,title):
    alert.title = title
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert)
    alert.open = True
    e.control.page.update()

tabela_movimentacoes = None

alert_confirm = ft.AlertDialog(
        modal=True,
        title=ft.Text("Deletar Movimentação"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.Container(content=(ft.TextButton("Sim",style=ft.ButtonStyle(color=ft.Colors.RED),
                                                     on_click=lambda e: deletar_movimentacao(e))),
                                                     border= ft.border.all(2,ft.Colors.RED),border_radius=15),
                 ft.TextButton("Não", on_click=lambda e: close_confirm(e))]
    )

def deletar_movimentacao(e):

    try:

        db_retornar_saldo_item(item_id_aux,mov_qtd_aux)
        db_deletar_movimentacao(mov_id_aux)  # Tenta deletar o item do banco de dados
        show_alert(e,ft.Text("Movimentação Deletada com Sucesso!", color=ft.Colors.GREEN))

        e.page.main_container.content = movimentacoes_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema
        show_alert(e,ft.Text(f"Erro ao deletar a Movimentação: {ex}", color=ft.Colors.RED))
        print(f"Erro ao deletar a Movimentação: {ex}")

def abrir_confirm(e, mov_id,pessoa_nome,item_nome,item_id,mov_qtd):

    global mov_id_aux, item_id_aux, mov_qtd_aux
    mov_id_aux  = mov_id
    item_id_aux = item_id
    mov_qtd_aux = mov_qtd

    alert_confirm.content = ft.Text(f"Deseja deletar a movimentação de '{pessoa_nome}'?\n {mov_qtd} Unidade(s) de '{item_nome}'.\n\n ATENÇÃO: O saldo do item será reajustado!!")
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert_confirm)
    alert_confirm.open = True
    e.control.page.update()

def close_confirm(e):
    alert_confirm.open = False
    e.control.page.update()

def item_selecionado(e):
    item = db_buscar_item(selected_item.value)
    total = item[0][2] - item[0][3]
    qtd_selected_item.value= f"Quantidade disponível: {total}"
    e.page.update()

def atualiza_filtros(e):
    atualiza_tabela_movimentacoes(filtro_pessoa.value,filtro_item.value)
    tabela_movimentacoes.update()
    e.page.update()

def cadastrar_movimentacao(e):
    if selected_pessoa.value and selected_item.value and int(qtd_textfield.value) > 0:

        # Verifica se o Item possui estoque suficiente         
        item = db_buscar_item(selected_item.value)
        item_qtd = item[0][2] - item[0][3] # (entrada - saída)
        if(item_qtd >= int(qtd_textfield.value)):

            db_adicionar_movimentacao(
                pessoa_id=selected_pessoa.value,
                item_id=selected_item.value,
                qtd=int(qtd_textfield.value),
                obs= obs_textfield.value
            )
            alert.title = ft.Text("Movimento Cadastrado com Sucesso!", color=ft.Colors.GREEN)
            db_diminuir_saldo_item(selected_item.value,int(qtd_textfield.value))
        else:   
            alert.title = ft.Text("Saldo do item insuficiente!", color=ft.Colors.RED)

        e.page.main_container.content = movimentacoes_view()
    else:
        alert.title = ft.Text("Preencha corretamente os campos!", color=ft.Colors.RED)
    
    e.control.page.overlay.clear()
    e.page.overlay.append(alert)
    alert.open = True
    e.page.update()

def atualiza_tabela_movimentacoes(filtro_pessoa = 0, filtro_item = 0):
    global tabela_movimentacoes

    movimentacoes = db_buscar_movimentacoes(filtro_pessoa,filtro_item)
    
    tabela_movimentacoes.rows.clear()

    for mov in movimentacoes:

        mov_id      = mov[0]
        pessoa_nome = mov[1]
        item_nome   = mov[2]
        item_id     = mov[6]
        mov_qtd     = mov[3]
        mov_obs     = mov[4]
        mov_data    = mov[5]


        tabela_movimentacoes.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(pessoa_nome)),
                    ft.DataCell(ft.Text(item_nome)),
                    ft.DataCell(ft.Text(mov_qtd)),
                    ft.DataCell( # Observação com Scroll
                        ft.Column(
                            controls=[ft.Text(
                                mov_obs,  
                                max_lines=None,
                                width=190,
                            )],
                            scroll=ft.ScrollMode.AUTO,
                            height=35,
                            width=200,
                        )
                    ),
                    ft.DataCell(ft.Text(mov_data)),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINED,
                        tooltip="Deletar pessoa",
                        on_click=lambda e, mov_id=mov_id,pessoa_nome = pessoa_nome, item_nome =item_nome,item_id = item_id, mov_qtd = mov_qtd: abrir_confirm(e, mov_id,pessoa_nome,item_nome,item_id,mov_qtd)
                        ))
                ]
            )
        )

def criar_tabela_movimentacoes():

    global tabela_movimentacoes
    tabela_movimentacoes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Usuário")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Quantidade"), numeric=True),
            ft.DataColumn(ft.Text("Observação")),
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text(""))
        ],
        rows=[]
    )

    atualiza_tabela_movimentacoes()

    return tabela_movimentacoes

def movimentacoes_view():
    global selected_pessoa, selected_item, qtd_textfield, qtd_selected_item, obs_textfield, filtro_pessoa, filtro_item, tabela
    pessoas = db_buscar_pessoas()
    itens = db_buscar_itens()

    selected_pessoa = ft.Dropdown(
        label="Selecione a Pessoa",
        options=[ft.dropdown.Option(str(p[0]), p[1]) for p in pessoas]
    )

    selected_item = ft.Dropdown(
        label="Selecione o Item",
        options=[ft.dropdown.Option(str(i[0]), i[1]) for i in itens],
        on_change=item_selecionado
    )

    filtro_pessoa = ft.Dropdown(
        label="Selecione uma pessoa para filtrar",
        options=[ft.dropdown.Option(str(p[0]), p[1]) for p in pessoas],
        on_change=atualiza_filtros
    )

    filtro_pessoa.options.insert(0,ft.dropdown.Option(0,"Todos"))
    filtro_pessoa.value = 0
    filtro_item = ft.Dropdown(
        label="Selecione um item para filtrar",
        options=[ft.dropdown.Option(str(i[0]), i[1]) for i in itens],
        on_change=atualiza_filtros
    )
    
    filtro_item.options.insert(0,ft.dropdown.Option(0,"Todos"))
    filtro_item.value = 0

    qtd_textfield = ft.TextField(label="Quantidade", input_filter=ft.NumbersOnlyInputFilter())
    obs_textfield = ft.TextField(label="Observação")
    qtd_selected_item = ft.Text("",size=14)

    tabela = ft.Column(controls=[criar_tabela_movimentacoes()], scroll=ft.ScrollMode.AUTO, height=650)
    
    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK87,
                padding=20,
                border_radius=15,
                content=ft.Column(
                    controls=[
                        ft.Text("Movimentações Registradas", size=24),
                        ft.Row(controls=[filtro_item,filtro_pessoa]),
                        tabela
                    ]
                )
            ),
            ft.Container(
                bgcolor=ft.Colors.BLACK87,
                padding=20,
                border_radius=15,
                content=ft.Column(
                    controls=[
                        ft.Text("Registrar Movimentação", size=24),
                        selected_pessoa,
                        selected_item,
                        qtd_selected_item,
                        qtd_textfield,
                        obs_textfield,
                        ft.ElevatedButton("Salvar Movimentação", on_click=cadastrar_movimentacao)
                    ]
                )
            )
        ]
    )
