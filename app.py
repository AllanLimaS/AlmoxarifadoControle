import flet as ft

from database.db import criar_tabelas

from views.pessoas_view import pessoas_view
from views.itens_view import itens_view
from views.movimentacoes_view import movimentacoes_view

main_container = ft.Container()

def main(page:ft.Page):

    criar_tabelas()

    page.main_container = ft.Container(
        content=itens_view(),
        expand=True,
        padding=20,
        border_radius=15
    )
    page.title = 'Controle de Estoque'
    page.window.maximized = True
    #page.window.title_bar_hidden = True
    page.padding = 0 

    def AtualizarHome(e):

        # verifica visual dos botões 
        for btn in menubar.controls:
            if isinstance(btn, ft.TextButton):
                if btn.data == e.control.data:
                    btn.disabled = True
                    btn.style = ft.ButtonStyle(bgcolor=ft.Colors.WHITE10)
                else:
                    btn.disabled = False
                    btn.style = ft.ButtonStyle(bgcolor=None)

        # executa função dos botões
        if e.control.data == 'item':
            page.main_container.content = itens_view()
        elif e.control.data == 'usuario':
            page.main_container.content = pessoas_view()
        elif e.control.data == 'movimentacoes':
            page.main_container.content = movimentacoes_view()

        page.update()

    menubar = ft.Row( 
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.TextButton("Itens", data ='item', on_click=AtualizarHome,icon=ft.Icons.FORMAT_LIST_NUMBERED_RTL_OUTLINED),
            ft.TextButton("Pessoas", data = 'usuario', on_click=AtualizarHome,icon=ft.Icons.PERSON),
            ft.TextButton("Movimentações", data = 'movimentacoes', on_click=AtualizarHome,icon=ft.Icons.IMPORT_EXPORT),

            ft.IconButton(
                    on_click=lambda e: page.window_close(),
                    icon='CLOSE',
                    icon_color= ft.Colors.RED,
                    width= 50,
                    height= 50
                )
        ]
    )


    page.add(
        ft.Column(
            controls=[
                menubar,
                page.main_container
            ]
        )
    )

if __name__ == '__main__':
    ft.app(target=main)
