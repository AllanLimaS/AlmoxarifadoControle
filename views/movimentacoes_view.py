import flet as ft

from database.db_movimentacoes import *
from database.db_itens import db_buscar_itens,db_buscar_item,db_diminuir_saldo_item
from database.db_pessoas import db_buscar_pessoas

alert = ft.AlertDialog(title=ft.Text("Movimento Cadastrado com Sucesso!"))

tabela_movimentacoes = None

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
        tabela_movimentacoes.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(mov[1])),
                    ft.DataCell(ft.Text(mov[2])),
                    ft.DataCell(ft.Text(mov[3])),
                    ft.DataCell( # Observação com Scroll
                        ft.Column(
                            controls=[ft.Text(
                                mov[4],  
                                max_lines=None,
                                width=190,
                            )],
                            scroll=ft.ScrollMode.AUTO,
                            height=35,
                            width=200,
                        )
                    ),
                    ft.DataCell(ft.Text(mov[5]))
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
            ft.DataColumn(ft.Text("Data"))
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
