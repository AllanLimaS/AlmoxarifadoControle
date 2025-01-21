import flet as ft

from database.db_usuario import *
from views.itens_view import itens_view  


alert = ft.AlertDialog(title=ft.Text(""))

def autenticar(e):

    if login_input.value != '' and senha_input.value != '': 
        autenticado = db_autenticar(login_input.value,senha_input.value)

        if autenticado:
            e.page.menubar.visible = True
            e.page.vertical_alignment = ft.MainAxisAlignment.START
            e.page.main_container.content = itens_view()
        else:
            erro_text.value = "Senha incorreta !"
    else:
        erro_text.value = "Preencha corretamente os campos !"
    e.page.update()

def cadastra(e):

    if login_input.value != '' and senha_input.value != '': 
        
        if senha_input.value == senha_confirm_input.value:
            db_adicionar_usuario(login_input.value,senha_input.value)
            e.page.main_container.content = login_view()
            e.page.update()
        else:

            e.control.page.overlay.clear()
            e.control.page.overlay.append(alert)
            alert.title = ft.Text("Senha não está batendo",color=ft.Colors.RED)
            alert.open = True
            e.control.page.update()
    else:

        e.control.page.overlay.clear()
        e.control.page.overlay.append(alert)
        alert.title = ft.Text("Necessário preencher corretamente os campos!",color=ft.Colors.RED)
        alert.open = True
        e.control.page.update()
    

def tela_cadastro_inicial_view():

    global login_input, senha_input, senha_confirm_input

    login_input = ft.TextField(label="Login", autofocus=True)
    senha_input = ft.TextField(label="Senha", password=True)
    senha_confirm_input = ft.TextField(label="Confirmar Senha", password=True)

    botao_salvar = ft.ElevatedButton("Salvar", on_click=cadastra)

    return ft.Container(
            bgcolor=ft.Colors.BLACK87,
            padding=40,
            border_radius=15,
            width=500,
            content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=
                [ft.Text("Cadastro Inicial",size=24,text_align=ft.TextAlign.CENTER,weight=ft.FontWeight.BOLD),
                ft.Container(height=30),
                login_input,
                senha_input,
                senha_confirm_input,
                botao_salvar])
        ) 

def login_view():

    if not db_usuario_existe():
        return tela_cadastro_inicial_view()

    else:
        usuario = db_buscar_usuario()
        
        global login_input, senha_input, erro_text

        login_input = ft.TextField(label="Login", autofocus=True, disabled=True, value=usuario[0][1])
        senha_input = ft.TextField(label="Senha", password=True)
        erro_text = ft.Text(color="red")
        botao_login = ft.ElevatedButton("Entrar", on_click=autenticar)

        return ft.Container(
            bgcolor=ft.Colors.BLACK87,
            padding=40,
            border_radius=15,
            width=500,
            content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=
                [ft.Text("Login",size=24,text_align=ft.TextAlign.CENTER,weight=ft.FontWeight.BOLD),
                ft.Container(height=30),
                login_input,
                senha_input,
                erro_text,
                botao_login])
        ) 