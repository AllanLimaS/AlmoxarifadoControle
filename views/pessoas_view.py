import flet as ft

from database.db_pessoas import *

nome_textfield = ft.TextField(label="Nome da Pessoa")

# textfields para alteração do usuario 
nome_new_textfield = ft.TextField(label="Alterar Nome")

alert = ft.AlertDialog(title=ft.Text("Pessoa Cadastrado com Sucesso!"))

alert_confirm = ft.AlertDialog(
        modal=True,
        title=ft.Text("Deletar Pessoa"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.Container(content=(ft.TextButton("Sim",style=ft.ButtonStyle(color=ft.Colors.RED),
                                                     on_click=lambda e: deletar_pessoa(e))),
                                                     border= ft.border.all(2,ft.Colors.RED),border_radius=15),
                 ft.TextButton("Não", on_click=lambda e: close_confirm(e))]
    )
alert_alterar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Alterar nome de pessoa"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.TextButton("Sim", on_click=lambda e: alterar_item(e)),
                 ft.TextButton("Não", on_click=lambda e: close_alterar(e))]
    )

def show_alert(e,title):
    alert.title = title
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert)
    alert.open = True
    e.control.page.update()

def close_confirm(e):
    alert_confirm.open = False
    e.control.page.update()

def close_alterar(e):
    alert_alterar.open = False
    e.control.page.update()

def alterar_item(e):
    
    try:
        db_alterar_pessoa(pessoa_id_aux,nome_new_textfield.value)

        show_alert(e,ft.Text("Pessoa alterada com Sucesso!", color=ft.Colors.GREEN))

        # Atualiza a visualização dos itens
        e.page.main_container.content = pessoas_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema

        show_alert(e,ft.Text(f"Erro ao alterar a pessoa: {ex}", color=ft.Colors.RED))
        print(f"Erro ao alterar a pessoa: {ex}")

def abrir_alterar(e,pessoa_id,pessoa_nome):

    global pessoa_id_aux 
    pessoa_id_aux = pessoa_id

    nome_new_textfield.value = pessoa_nome

    alert_alterar.content = ft.Column(controls=[
                                ft.Text(f"Alterar o nome da pessoa: '{pessoa_nome}'"),
                                nome_new_textfield,
                                ],
                                height=100)  
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert_alterar)
    alert_alterar.open = True
    e.control.page.update()

def deletar_pessoa(e):
    try:
        db_deletar_pessoa(id_pessoa_aux)  # Tenta deletar o item do banco de dados
        show_alert(e,ft.Text("Pessoa Deletado com Sucesso!", color=ft.Colors.GREEN))

        # Atualiza a visualização dos itens
        e.page.main_container.content = pessoas_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema
        show_alert(e,ft.Text(f"Erro ao deletar a pessoa: {ex}", color=ft.Colors.GREEN))
        print(f"Erro ao deletar a pessoa: {ex}")  # Ou use um sistema de logs

def abrir_confirm(e,pessoa_id,pessoa_nome):

    global id_pessoa_aux 
    id_pessoa_aux = pessoa_id
    alert_confirm.content = ft.Text(f"Deseja deletar o item '{pessoa_nome}'?\n\n ATENÇÃO: Todos os movimentos relacionados a essa pessoa serão excluídos!")
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert_confirm)
    alert_confirm.open = True
    e.control.page.update()

def carregar_pessoas():

    dataTable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("")),
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
                        icon=ft.Icons.CREATE,
                        tooltip="Alterar item",
                        on_click=lambda e, pessoa_id=pessoa_id,pessoa_nome = pessoa_nome: abrir_alterar(e, pessoa_id,pessoa_nome)
                        )),
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