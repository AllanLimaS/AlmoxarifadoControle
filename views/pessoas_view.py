import flet as ft

def pessoas_view():
    return ft.Column(
        controls=[
            ft.Text("Tela de Cadastro de Pessoas", size=24),
            ft.TextField(label="Nome"),
            ft.TextField(label="Idade"),
            ft.ElevatedButton("Salvar", on_click=lambda e: print("Pessoa salva!"))
        ]
    )