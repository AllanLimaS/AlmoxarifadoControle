import flet as ft

from database.db import db_adicionar_item, db_buscar_itens, db_deletar_item

nome_textfield = ft.TextField(label="Nome do Item")
qtd_textfield = ft.TextField(label="Quantidade", input_filter=ft.NumbersOnlyInputFilter())

alert = ft.AlertDialog(title=ft.Text("Item Cadastrado com Sucesso!"))

alert_confirm = ft.AlertDialog(
        modal=True,
        title=ft.Text("Deletar Item"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.TextButton("Yes", on_click=lambda e: deletar_item(e)),
                 ft.TextButton("No", on_click=lambda e: close_confirm(e))]
    )

def close_confirm(e):
    alert_confirm.open = False
    e.control.page.update()

def deletar_item(e):

    try:
        db_deletar_item(id_item_aux)  # Tenta deletar o item do banco de dados
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("Item Deletado com Sucesso!", color=ft.Colors.GREEN)
        e.control.page.overlay.append(alert)
        alert.open = True

        # Atualiza a visualização dos itens
        e.page.main_container.content = itens_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema
        alert.title = ft.Text(f"Erro ao deletar o item: {ex}", color=ft.Colors.RED)
        e.control.page.overlay.append(alert)
        alert.open = True
        e.control.page.update()
        print(f"Erro ao deletar o item: {ex}")  # Ou use um sistema de logs

def abrir_confirm(e,item_id,nome_item):

    global id_item_aux 
    id_item_aux = item_id
    alert_confirm.content = ft.Text(f"Deseja deletar o item '{nome_item}'?")

    e.control.page.overlay.append(alert_confirm)
    alert_confirm.open = True
    e.control.page.update()

def carregar_itens():

    dataTable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Quantidade"),numeric=True),
            ft.DataColumn(ft.Text(""))
        ]
    )

    itens = db_buscar_itens()
    itens = sorted(itens, key=lambda x: x[1], reverse=False)

    for item in itens:

        item_id = item[0]  
        nome_item = item[1]  
        quantidade = item[2]  

        dataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(nome_item)),
                    ft.DataCell(ft.Text(quantidade)),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINED,
                        tooltip="Deletar item",
                        on_click=lambda e, item_id=item_id,nome_item = nome_item: abrir_confirm(e, item_id,nome_item)
                        ))
                ]
            )
        )



    gridItens = ft.Column(
        controls=[dataTable],
        scroll=ft.ScrollMode.AUTO,  # Permite scroll
        height=400  # Defina a altura para ativar o scroll
    )
    return gridItens

def cadastra_item(e):

    global main_container
    
    if nome_textfield.value != '' and qtd_textfield.value != '': 
        db_adicionar_item(nome_textfield.value,qtd_textfield.value)
        nome_textfield.value = ''
        qtd_textfield.value = ''

        alert.title = ft.Text("Item Cadastrado com Sucesso!", color=ft.Colors.GREEN)
        e.control.page.overlay.append(alert)
        alert.open = True

        e.page.main_container.content = itens_view()
        e.page.update()

    else:

        alert.title = ft.Text("Necessário preencher corretamente os campos!",color=ft.Colors.RED)
        e.control.page.overlay.append(alert)
        alert.open = True
        e.control.page.update()
        
def itens_view():
        global gridItens

        gridItens = carregar_itens()

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
                            ft.Text("Itens Cadastrados", size=24),
                            gridItens
                        ],
                    )
                ),

                ft.Container(
                    bgcolor=ft.Colors.BLACK87,
                    padding=20,
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            ft.Text("Cadastrar Novo Item", size=24),
                            nome_textfield,
                            qtd_textfield,
                            ft.ElevatedButton("Salvar", on_click=cadastra_item )
                        ]
                    )
                )
            ]
        )