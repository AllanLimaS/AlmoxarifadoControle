import flet as ft
from database.db import db_buscar_pessoas, db_buscar_itens, db_adicionar_movimentacao, db_buscar_movimentacoes

alert = ft.AlertDialog(title=ft.Text("Item Cadastrado com Sucesso!"))


def cadastrar_movimentacao(e):
    if selected_pessoa.value and selected_item.value and qtd_textfield.value:
        db_adicionar_movimentacao(
            pessoa_id=selected_pessoa.value,
            item_id=selected_item.value,
            quantidade=int(qtd_textfield.value)
        )
        e.page.overlay.append(alert)
        alert.open = True

        e.page.main_container.content = movimentacoes_view()
        e.page.update()
    else:
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

    return ft.Column(controls=[dataTable], scroll=ft.ScrollMode.AUTO, height=400)

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
