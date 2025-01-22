import flet as ft

from database.db_itens import *
from controlls.report import gerar_relatorio_itens

# textfields para cadastro do item 
nome_textfield = ft.TextField(label="Nome do Item")
qtd_textfield = ft.TextField(label="Entrada", input_filter=ft.NumbersOnlyInputFilter())

# textfields para alteração do item 
entrada_new_textfield = ft.TextField(label="Alterar Entrada", input_filter=ft.NumbersOnlyInputFilter())
saida_new_textfield = ft.TextField(label="Alterar Saída", input_filter=ft.NumbersOnlyInputFilter())

# alertas / popups 
alert = ft.AlertDialog(title=ft.Text("Item Cadastrado com Sucesso!"))

alert_confirm = ft.AlertDialog(
        modal=True,
        title=ft.Text("Deletar Item"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.Container(content=(ft.TextButton("Sim",style=ft.ButtonStyle(color=ft.Colors.RED),
                                                     on_click=lambda e: deletar_item(e))),
                                                     border= ft.border.all(2,ft.Colors.RED),border_radius=15),
                 ft.TextButton("Não", on_click=lambda e: close_confirm(e))]
    )
alert_alterar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Alterar estoque de Item"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[ft.TextButton("Sim", on_click=lambda e: alterar_item(e)),
                 ft.TextButton("Não", on_click=lambda e: close_alterar(e))]
    )

def close_confirm(e):
    alert_confirm.open = False
    e.control.page.update()

def close_alterar(e):
    alert_alterar.open = False
    e.control.page.update()

def alterar_item(e):
    
    try:
        db_alterar_saldo_item(id_item_aux,entrada_new_textfield.value,saida_new_textfield.value)
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("Item alterado com Sucesso!", color=ft.Colors.GREEN)
        alert.open = True

        # Atualiza a visualização dos itens
        e.page.main_container.content = itens_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema
        alert.title = ft.Text(f"Erro ao alterar o item: {ex}", color=ft.Colors.RED)
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.open = True
        e.control.page.update()
        print(f"Erro ao deletar o item: {ex}")

def deletar_item(e):

    try:
        db_deletar_item(id_item_aux)  # Tenta deletar o item do banco de dados
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("Item Deletado com Sucesso!", color=ft.Colors.GREEN)
        alert.open = True

        # Atualiza a visualização dos itens
        e.page.main_container.content = itens_view()
        e.page.update()
    except Exception as ex:
        # Exibe uma mensagem de erro e registra o problema
        alert.title = ft.Text(f"Erro ao deletar o item: {ex}", color=ft.Colors.RED)
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.open = True
        e.control.page.update()
        print(f"Erro ao deletar o item: {ex}")

def abrir_confirm(e,item_id,nome_item):

    global id_item_aux 
    id_item_aux = item_id
    alert_confirm.content = ft.Text(f"Deseja deletar o item '{nome_item}'?\n\n ATENÇÃO: Todos os movimentos relacionados a esse item serão excluídos!")
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert_confirm)
    alert_confirm.open = True
    e.control.page.update()

def abrir_alterar(e,item_id,item_nome,item_entrada,item_saida):

    global id_item_aux 
    id_item_aux = item_id

    entrada_new_textfield.value = item_entrada
    saida_new_textfield.value = item_saida

    alert_alterar.content = ft.Column(controls=[
                                ft.Text(f"O item '{item_nome}' possui:"),
                                ft.Text(f"Entrada '{item_entrada}' unidades."),
                                entrada_new_textfield,
                                ft.Text(f"Saída '{item_saida}' unidades."),
                                saida_new_textfield
                                ],
                                height=200)  
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert_alterar)
    alert_alterar.open = True
    e.control.page.update()

def carregar_itens():

    dataTable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Entrada"),numeric=True),
            ft.DataColumn(ft.Text("Saída"),numeric=True),
            ft.DataColumn(ft.Text("Total"),numeric=True),
            ft.DataColumn(ft.Text("")), # espaço para o botão de alterar 
            ft.DataColumn(ft.Text("")) # espaço para o botão de excluir
        ]
    )

    itens = db_buscar_itens()
    itens = sorted(itens, key=lambda x: x[1], reverse=False)

    for item in itens:

        item_id = item[0]  
        nome_item = item[1]  
        entrada = item[2]
        saida = item[3]  
        total = entrada - saida

        dataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(nome_item)),
                    ft.DataCell(ft.Text(entrada)),
                    ft.DataCell(ft.Text(saida)),
                    ft.DataCell(ft.Text(total)),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.CREATE,
                        tooltip="Alterar item",
                        on_click=lambda e, item_id=item_id,nome_item = nome_item, entrada = entrada, saida = saida: abrir_alterar(e, item_id,nome_item,entrada,saida)
                        )),
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
        height=650  # Defina a altura para ativar o scroll
    )
    return gridItens

def cadastra_item(e):

    global main_container
    
    if nome_textfield.value != '' and qtd_textfield.value != '': 
        db_adicionar_item(nome_textfield.value,qtd_textfield.value)
        nome_textfield.value = ''
        qtd_textfield.value = ''

        alert.title = ft.Text("Item Cadastrado com Sucesso!", color=ft.Colors.GREEN)
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.open = True

        e.page.main_container.content = itens_view()
        e.page.update()

    else:

        alert.title = ft.Text("Necessário preencher corretamente os campos!",color=ft.Colors.RED)
        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.open = True
        e.control.page.update()
        
def gerar_relatorio(e):
    lista_itens = db_buscar_itens()
    path_pdf = gerar_relatorio_itens(lista_itens)
    alert.title = ft.Text(f"Relatório salvo em: {path_pdf}",color=ft.Colors.GREEN_ACCENT)
    e.control.page.overlay.clear()
    e.control.page.overlay.append(alert)
    alert.open = True
    e.control.page.update()

def gerar_relatorio_simples(e):
    lista_itens = db_buscar_itens()
    path_pdf = gerar_relatorio_itens(lista_itens)
    alert.title = ft.Text(f"Relatório salvo em: {path_pdf}",color=ft.Colors.GREEN_ACCENT)
    e.control.page.overlay.clear()
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

                ft.Column(
                    controls=[
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
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.BLACK87,
                            padding=20,
                            border_radius=15,
                            content=ft.Column(
                                controls=[
                                    ft.ElevatedButton("Gerar Relatório (PDF)", on_click=gerar_relatorio),
                                    ft.ElevatedButton("Gerar Relatório simples (PDF)", on_click=gerar_relatorio_simples)
                                ]
                            )
                        )
                    ]
                )
                
            ]
        )