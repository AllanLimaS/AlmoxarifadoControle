import flet as ft

from database.db_pessoas import *

nome_textfield = ft.TextField(label="Nome da Pessoa")

alert = ft.AlertDialog(title=ft.Text("Pessoa Cadastrado com Sucesso!"))

alert_confirm = ft.AlertDialog(
        modal=True,
        title=ft.Text("Deletar Pessoa"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.TextButton("Yes", on_click=lambda e: deletar_pessoa(e)),
                 ft.TextButton("No", on_click=lambda e: close_confirm(e))]
    )

def close_confirm(e):
    alert_confirm.open = False
    e.control.page.update()

def deletar_pessoa(e):
    try:
        db_deletar_pessoa(id_pessoa_aux)  # Tenta deletar o item do banco de dados
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("pessoa Deletado com Sucesso!", color=ft.Colors.GREEN)
        alert.open = True

        # Atualiza a visualização dos itens
        e.page.main_container.content = pessoas_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema
        alert.title = ft.Text(f"Erro ao deletar a pessoa: {ex}", color=ft.Colors.RED)
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.open = True
        e.control.page.update()
        print(f"Erro ao deletar a pessoa: {ex}")  # Ou use um sistema de logs

def abrir_confirm(e,pessoa_id,pessoa_nome):

    global id_pessoa_aux 
    id_pessoa_aux = pessoa_id
    alert_confirm.content = ft.Text(f"Deseja deletar o item '{pessoa_nome}'?")

    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert_confirm)
    alert_confirm.open = True
    e.control.page.update()

def carregar_pessoas():

    dataTable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text(""))
        ]
    )

    pessoas = db_buscar_pessoas()
    pessoas = sorted(pessoas, key=lambda x: x[1], reverse=False)

    for pessoa in pessoas:

        pessoa_id = pessoa[0]  
        pessoa_nome = pessoa[1]  

        dataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(pessoa_nome)),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINED,
                        tooltip="Deletar pessoa",
                        on_click=lambda e, pessoa_id=pessoa_id,pessoa_nome = pessoa_nome: abrir_confirm(e, pessoa_id,pessoa_nome)
                        ))
                ]
            )
        )



    gridPessoas = ft.Column(
        controls=[dataTable],
        scroll=ft.ScrollMode.AUTO,  # Permite scroll
        height=650  # Defina a altura para ativar o scroll
    )
    return gridPessoas

def cadastra_pessoa(e):

    global main_container
    
    if nome_textfield.value != '': 
        db_adicionar_pessoa(nome_textfield.value)
        nome_textfield.value = ''

        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("Pessoa Cadastrada com Sucesso!", color=ft.Colors.GREEN)
        alert.open = True

        e.page.main_container.content = pessoas_view()
        e.page.update()

    else:

        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("Necessário preencher corretamente os campos!",color=ft.Colors.RED)
        alert.open = True
        e.control.page.update()
        
def pessoas_view():
        global gridpessoas

        gridpessoas = carregar_pessoas()

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
                            ft.Text("Pessoas Cadastradas", size=24),
                            gridpessoas
                        ],
                    )
                ),

                ft.Container(
                    bgcolor=ft.Colors.BLACK87,
                    padding=20,
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            ft.Text("Cadastrar Nova Pessoa", size=24),
                            nome_textfield,
                            ft.ElevatedButton("Salvar", on_click=cadastra_pessoa )
                        ]
                    )
                )
            ]
        )