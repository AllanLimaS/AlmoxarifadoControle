import flet as ft

from database.db_movimentacoes import *
from database.db_itens import db_buscar_itens,db_buscar_item,db_diminuir_saldo_item
from database.db_pessoas import db_buscar_pessoas

alert = ft.AlertDialog(title=ft.Text("Movimento Cadastrado com Sucesso!"))


def cadastrar_movimentacao(e):
    if selected_pessoa.value and selected_item.value and int(qtd_textfield.value) > 0:

        # Verifica se o Item possui estoque suficiente         
        item = db_buscar_item(selected_item.value)
        item_qtd = item[0][2]
        if(item_qtd >= int(qtd_textfield.value)):

            db_adicionar_movimentacao(
                pessoa_id=selected_pessoa.value,
                item_id=selected_item.value,
                quantidade=int(qtd_textfield.value)
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

def carregar_movimentacoes():
    dataTable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Usuário")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Quantidade"), numeric=True),
            ft.DataColumn(ft.Text("Data"))
        ]
    )

    movimentacoes = db_buscar_movimentacoes()
    for mov in movimentacoes:
        dataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(mov[1])),
                    ft.DataCell(ft.Text(mov[2])),
                    ft.DataCell(ft.Text(mov[3])),
                    ft.DataCell(ft.Text(mov[4]))
                ]
            )
        )

    return ft.Column(controls=[dataTable], scroll=ft.ScrollMode.AUTO, height=650)

def movimentacoes_view():
    global selected_pessoa, selected_item, qtd_textfield
    pessoas = db_buscar_pessoas()
    itens = db_buscar_itens()

    selected_pessoa = ft.Dropdown(
        label="Selecione a Pessoa",
        options=[ft.dropdown.Option(str(p[0]), p[1]) for p in pessoas]
    )

    selected_item = ft.Dropdown(
        label="Selecione o Item",
        options=[ft.dropdown.Option(str(i[0]), i[1]) for i in itens]
    )

    qtd_textfield = ft.TextField(label="Quantidade", input_filter=ft.NumbersOnlyInputFilter())

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
                        ft.Text("Registrar Movimentação", size=24),
                        selected_pessoa,
                        selected_item,
                        qtd_textfield,
                        ft.ElevatedButton("Salvar Movimentação", on_click=cadastrar_movimentacao)
                    ]
                )
            ),
            ft.Container(
                bgcolor=ft.Colors.BLACK87,
                padding=20,
                border_radius=15,
                content=ft.Column(
                    controls=[
                        ft.Text("Movimentações Registradas", size=24),
                        carregar_movimentacoes()
                    ]
                )
            )
        ]
    )
